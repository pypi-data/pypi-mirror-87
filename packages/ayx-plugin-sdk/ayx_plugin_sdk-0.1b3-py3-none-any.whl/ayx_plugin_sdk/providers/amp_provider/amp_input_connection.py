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
"""AMP SDK Input Connection Class."""
import logging
from typing import Optional, TYPE_CHECKING

from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.core.input_connection_base import InputConnectionBase

if TYPE_CHECKING:
    from ayx_plugin_sdk.core import Metadata  # noqa: F401
    from ayx_plugin_sdk.core.input_connection_base import InputConnectionStatus
    from ayx_plugin_sdk.core.record_packet_base import RecordPacketBase
    from ayx_plugin_sdk.providers.amp_provider.amp_input_anchor import AMPInputAnchor


logger = logging.getLogger(__name__)


@inherit_docs
class AMPInputConnection(InputConnectionBase):
    """Class for managing Inputs in AMP SDK provider."""

    def __init__(
        self, name: str, metadata: "Metadata", anchor: "AMPInputAnchor"
    ) -> None:
        """
        Instantiate an AMP provider input connection.

        Parameters
        ----------
        name
            Name of the input connection.
        metadata
            Metadata for the input connections.
        anchor
            Input anchor associated with this connection.
        """
        self.__name = name
        self.__metadata = metadata  # TODO: Get metadata from repository
        self.__anchor = anchor
        self.progress = 0.0

    @property
    def name(self) -> str:  # noqa: D102
        return self.__name

    @property
    def metadata(self) -> Optional["Metadata"]:  # noqa: D102
        return self.__metadata

    @property
    def anchor(self) -> "AMPInputAnchor":  # noqa: D102
        return self.__anchor

    def read(self) -> "RecordPacketBase":  # noqa: D102
        if self.metadata is None:
            raise RuntimeError("Input connection has not been opened yet.")
        logger.debug(
            f"Reading record packet from input connection {self.name} on input anchor {self.anchor.name}"
        )
        from ayx_plugin_sdk.providers.amp_provider.repositories.input_record_packet_repository import (
            EmptyRecordPacketRepositoryException,
            InputRecordPacketRepository,
        )

        try:
            packet = InputRecordPacketRepository().peek_record_packet(
                self.anchor.name, self.name
            )
        except EmptyRecordPacketRepositoryException:
            raise RuntimeError("All record packets have been read from this connection")
        return packet

    def _get_max_packet_size(self) -> Optional[int]:
        from ayx_plugin_sdk.providers.amp_provider.repositories import (
            InputConnectionRepository,
        )

        try:
            return InputConnectionRepository().get_connection_packet_size(
                self.anchor.name, self.name
            )
        except ValueError:
            return None

    def _set_max_packet_size(self, value: Optional[int]) -> None:
        if value and value <= 0:
            raise ValueError(
                "max_packet_size must be None or an integer greater than 0."
            )

        from ayx_plugin_sdk.providers.amp_provider.repositories import (
            InputConnectionRepository,
        )

        InputConnectionRepository().save_connection_packet_size(
            self.anchor.name, self.name, value
        )

    @property
    def progress(self) -> float:  # noqa: D102
        return self.__progress

    @progress.setter
    def progress(self, value: float) -> None:  # noqa: D102
        if value < 0:
            raise ValueError("Progress percentage must be greater than 0.")
        self.__progress = value

    @property
    def status(self) -> "InputConnectionStatus":
        """Return connection status as enum."""
        from ayx_plugin_sdk.providers.amp_provider.repositories import (
            InputConnectionRepository,
        )

        return InputConnectionRepository().get_connection_status(
            self.anchor.name, self.name
        )
