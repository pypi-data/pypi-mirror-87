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
"""SDK Engine service grpc class."""
import logging
import traceback
from typing import Any, Callable

from ayx_plugin_sdk.providers.amp_provider import AMPDriver, AMPProvider
from ayx_plugin_sdk.providers.amp_provider.repositories import (
    EnvironmentRepository,
    InputAnchorRepository,
    InputConnectionRepository,
    InputMetadataRepository,
    InputRecordPacketRepository,
    OutputAnchorRepository,
    OutputMetadataRepository,
    OutputRecordPacketRepository,
    ToolConfigRepository,
)
from ayx_plugin_sdk.providers.amp_provider.resources.generated.sdk_tool_service_pb2_grpc import (
    SdkToolServicer,
)
from ayx_plugin_sdk.providers.amp_provider.resources.generated.transport_pb2 import (
    ReturnStatus,
)
from ayx_plugin_sdk.tracer_bullet.tracer_bullet_plugin import TracerBulletPlugin

import grpc


logger = logging.getLogger()


def _handle_service_exception(method: Callable) -> Callable:
    def _handle_exception(obj, request, context) -> Any:  # type: ignore
        try:
            return method(obj, request, context)
        except Exception:
            traceback_str = traceback.format_exc()
            logger.exception(traceback_str)
            context.set_details(traceback_str)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.abort(code=grpc.StatusCode.INTERNAL, details=traceback_str)

    return _handle_exception


def clear_all_repositories() -> None:
    """Clear all repositories in-between workflow runs."""
    EnvironmentRepository().clear_repository()
    InputAnchorRepository().clear_repository()
    InputConnectionRepository().clear_repository()
    InputMetadataRepository().clear_repository()
    InputRecordPacketRepository().clear_repository()
    OutputAnchorRepository().clear_repository()
    OutputMetadataRepository().clear_repository()
    OutputRecordPacketRepository().clear_repository()
    ToolConfigRepository().clear_repository()


class SdkToolService(SdkToolServicer):
    """SDK Tool Service GRPC overrides."""

    @_handle_service_exception
    def ConfirmSdkToolServiceConnection(self, request, context):  # type: ignore # noqa: N802
        """Confirm healthy connection."""
        logger.debug("ConfirmSdkToolServiceConnection called.")
        status = ReturnStatus(message=f"Connection successful!", success=True)
        return status

    @_handle_service_exception
    def InitializeSdkPlugin(self, request, context):  # type: ignore # noqa: N802
        """Initialize SDK plugin with config, anchors, and connections."""
        logger.debug("InitializeSdkPlugin called.")
        AMPDriver().clear_state()
        clear_all_repositories()

        ToolConfigRepository().save_xml_tool_config(request.configXml)
        EnvironmentRepository().save_engine_constants(dict(request.engineConstants))
        EnvironmentRepository().save_update_mode(request.updateMode)

        for input_anchor in request.incomingAnchors:
            logger.debug(f"Saving input anchor: \n{input_anchor}\n")
            InputAnchorRepository().save_grpc_anchor(input_anchor)

        for output_anchor in request.outgoingAnchors:
            logger.debug(f"Saving output anchor: \n{output_anchor}\n")
            OutputAnchorRepository().save_grpc_anchor(output_anchor)

        amp_provider = AMPProvider()
        sdk_plugin = TracerBulletPlugin(amp_provider)
        AMPDriver().plugin = sdk_plugin

        for anchor in request.incomingAnchors:
            for connection in anchor.connections:
                logger.debug(
                    f"Driving metadata for input anchor {anchor.name} and connection {connection.name}."
                )
                AMPDriver().metadata_received(anchor.name, connection.name)

        status = ReturnStatus(message=f"Initialization successful!", success=True)
        return status

    @_handle_service_exception
    def PushIncomingRecordPacket(self, request, context):  # type: ignore # noqa: N802
        """Push a record packet to the plugin."""
        logger.debug("PushIncomingRecordPacket called.")
        logger.debug(
            f"Packet received on anchor {request.anchor_name} and connection {request.connection_name}."
        )
        record_packet_metadata = InputMetadataRepository().get_metadata(
            request.anchor_name, request.connection_name
        )
        InputRecordPacketRepository().save_grpc_record_packet(
            anchor_name=request.anchor_name,
            connection_name=request.connection_name,
            grpc_record_packet=request.record_packet,
            metadata=record_packet_metadata,
        )
        logger.debug(
            f"Driving record packet to plugin on anchor {request.anchor_name} and connection {request.connection_name}."
        )
        AMPDriver().record_packet_received(
            anchor_name=request.anchor_name, connection_name=request.connection_name,
        )
        status = ReturnStatus(message="Record packet recieved!", success=True)
        return status

    @_handle_service_exception
    def NotifyIncomingConnectionComplete(self, request, context):  # type: ignore # noqa: N802
        """Notify the plugin that a connection has closed."""
        logger.debug("NotifyIncomingConnectionComplete called.")
        logger.debug(
            f"Connection closed for anchor {request.anchor_name}, connection {request.connection_name}"
        )
        AMPDriver().connection_closed_callback(
            request.anchor_name, request.connection_name
        )
        logger.debug(
            f"Connection closed for anchor {request.anchor_name}, connection {request.connection_name}"
        )
        status = ReturnStatus(
            message=f"Connection {request.connection_name} closed!", success=True
        )
        return status

    @_handle_service_exception
    def NotifyPluginComplete(self, request, context):  # type: ignore # noqa: N802
        """Notify the plugin that the on_complete method should be called."""
        logger.debug("NotifyPluginComplete Called")
        AMPDriver().complete_callback()
        status = ReturnStatus(message=f"Plugin process complete!", success=True)
        return status
