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
"""Repository for the status of the handshake with the SDK engine server."""
import logging
from typing import Dict, Optional, TYPE_CHECKING, cast

from ayx_plugin_sdk.providers.amp_provider import AMPRecordPacket
from ayx_plugin_sdk.providers.amp_provider.builders import (
    MetadataBuilder,
    RecordPacketBuilder,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.singleton import Singleton


if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.grpc_util import SocketAddress
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.record_packet_pb2 import (
        RecordPacket as ProtobufRecordPacket,
    )
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.metadata_pb2 import (
        Metadata as ProtobufMetadata,
    )
    from ayx_plugin_sdk.core import Metadata as CoreMetadata  # noqa: F401

logger = logging.getLogger(__name__)


class TestHarnessStateRepository(metaclass=Singleton):
    """
    Class defines methods and properties to read/write/delete the handshake status.

    NOTE: This class is only used by the test harness and shouldn't be used by the
    SDK Tool Service.
    """

    __test__ = False  # Pytest tries to collect this by default, disable here to prevent warning

    def __init__(self) -> None:
        """Construct the repository."""
        self._handshake_completed = False
        self._sdk_tool_server_address: Optional["SocketAddress"] = None
        self._metadata: Dict[str, "CoreMetadata"] = {}
        self._record_packets: Dict[str, "AMPRecordPacket"] = {}

    def save_handshake_completed_status(self, status: bool) -> None:
        """Save handshake completed status."""
        logger.debug(f"Handshake completed: {status}")
        self._handshake_completed = status

    def get_handshake_completed_status(self) -> bool:
        """Save AMP input anchor to repository."""
        return self._handshake_completed

    def save_sdk_tool_server_address(self, address: "SocketAddress") -> None:
        """Save the SDK Tool server address."""
        self._sdk_tool_server_address = address

    def get_sdk_tool_server_address(self) -> "SocketAddress":
        """Get the SDK Tool server address."""
        if self._sdk_tool_server_address is None:
            raise ValueError("SDK Tool server address has not been saved.")

        return self._sdk_tool_server_address

    def save_metadata(self, anchor_name: str, metadata: "ProtobufMetadata") -> None:  # type: ignore
        core_metadata = MetadataBuilder().from_protobuf(metadata)
        logger.debug(f"Saving metadata {core_metadata} to TestHarnessStateRepository")
        self._metadata[anchor_name] = core_metadata

    def get_metadata(self, anchor_name: str) -> "CoreMetadata":
        if anchor_name not in self._metadata:
            raise ValueError(f"Anchor name '{anchor_name}' not found.")
        return self._metadata[anchor_name]

    def save_record_packet(
        self, anchor_name: str, record_packet: "ProtobufRecordPacket"  # type: ignore
    ) -> None:
        core_record_packet, _, _ = RecordPacketBuilder().from_protobuf(
            record_packet, self.get_metadata(anchor_name)
        )
        self._record_packets[anchor_name] = cast(AMPRecordPacket, core_record_packet)

    def get_record_packet(self, anchor_name: str) -> "AMPRecordPacket":
        if anchor_name not in self._record_packets:
            raise ValueError(f"Anchor name '{anchor_name}' not found")
        logger.debug(f"Saving record packet for {anchor_name}")
        return self._record_packets[anchor_name]
