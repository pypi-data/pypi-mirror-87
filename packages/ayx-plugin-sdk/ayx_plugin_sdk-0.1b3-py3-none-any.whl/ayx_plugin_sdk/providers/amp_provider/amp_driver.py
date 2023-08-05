# Copyright (C) 2020 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""AMP Driver definition."""
import logging
import traceback
from typing import Optional

from ayx_plugin_sdk.core import Plugin
from ayx_plugin_sdk.core.exceptions import WorkflowRuntimeError
from ayx_plugin_sdk.core.input_connection_base import InputConnectionStatus
from ayx_plugin_sdk.providers.amp_provider.repositories import (
    IORepository,
    InputConnectionRepository,
    InputRecordPacketRepository,
    Singleton,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.input_record_packet_repository import (
    EmptyRecordPacketRepositoryException,
    UnfinishedRecordPacketException,
)

logger = logging.getLogger(__name__)


class AMPDriver(metaclass=Singleton):
    """The AMP Driver is a class that manages the lifecycle methods of a plugin instance."""

    def __init__(self) -> None:
        self.__plugin: Optional["Plugin"] = None

    @staticmethod
    def _workflow_error(exception: WorkflowRuntimeError) -> None:
        tb = traceback.format_tb(exception.__traceback__)
        IORepository().save_error("".join(["\n"] + tb[1:]))

    def metadata_received(self, anchor_name: str, connection_name: str) -> None:
        """Retrieve the input connection, and calls plugin's on_input_connection_initialized method."""
        connection = InputConnectionRepository().get_connection(
            anchor_name, connection_name
        )

        InputConnectionRepository().save_connection_status(
            anchor_name, connection_name, InputConnectionStatus.INITIALIZED
        )
        logger.debug(f"Connection {connection_name} on {anchor_name} initialized")
        try:
            self.plugin.on_input_connection_opened(connection)
        except WorkflowRuntimeError as e:
            self._workflow_error(e)

    def record_packet_received(self, anchor_name: str, connection_name: str) -> None:
        """Retrieve input connection, and calls plugin's on_record_packet method."""
        connection = InputConnectionRepository().get_connection(
            anchor_name, connection_name
        )
        InputConnectionRepository().save_connection_status(
            anchor_name, connection_name, InputConnectionStatus.RECEIVING_RECORDS
        )
        logger.debug(
            f"Connection {connection_name} on anchor {anchor_name} receiving records"
        )
        while True:
            try:
                InputRecordPacketRepository().peek_record_packet(
                    anchor_name, connection_name
                )
            except (
                UnfinishedRecordPacketException,
                EmptyRecordPacketRepositoryException,
            ):
                break
            else:
                logger.debug(
                    f"Sending record packet to connection {connection_name} on anchor {anchor_name}"
                )
                try:
                    self.plugin.on_record_packet(connection)
                except WorkflowRuntimeError as e:
                    self._workflow_error(e)
                InputRecordPacketRepository().pop_record_packet(
                    anchor_name, connection_name
                )

    def connection_closed_callback(
        self, anchor_name: str, connection_name: str
    ) -> None:
        """Close individual connections."""
        InputConnectionRepository().save_connection_status(
            anchor_name, connection_name, InputConnectionStatus.CLOSED
        )
        logger.debug(f"Closed connection {connection_name} on anchor {anchor_name}")
        try:
            InputRecordPacketRepository().peek_record_packet(
                anchor_name, connection_name
            )
        except EmptyRecordPacketRepositoryException:
            pass
        else:
            try:
                self.plugin.on_record_packet(
                    InputConnectionRepository().get_connection(
                        anchor_name, connection_name
                    )
                )
            except WorkflowRuntimeError as e:
                self._workflow_error(e)

    def complete_callback(self) -> None:
        """Call plugin's on_complete method."""
        logger.debug(f"Plugin complete, closing")
        try:
            self.plugin.on_complete()
        except WorkflowRuntimeError as e:
            self._workflow_error(e)

    @property
    def plugin(self) -> "Plugin":
        """Get the plugin associated with this driver."""
        if self.__plugin is None:
            raise ValueError("Plugin has not been initialized")
        return self.__plugin

    @plugin.setter
    def plugin(self, value: "Plugin") -> None:
        """Set the plugin associated with this driver."""
        self.__plugin = value
        logger.debug(f"Assigned plugin {value}")

    def clear_state(self) -> None:
        """Reset the AMP Driver."""
        self.__plugin = None
