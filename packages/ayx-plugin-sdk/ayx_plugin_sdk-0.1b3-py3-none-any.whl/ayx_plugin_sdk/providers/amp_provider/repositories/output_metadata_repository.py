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
"""Class that saves output metadata information given the associated anchor name."""
import logging
from typing import Dict, TYPE_CHECKING

from ayx_plugin_sdk.providers.amp_provider.builders.metadata_builder import (
    MetadataBuilder,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.grpc_repository import (
    GrpcRepository,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.singleton import Singleton
from ayx_plugin_sdk.providers.amp_provider.resources.generated.outgoing_metadata_push_pb2 import (
    OutgoingMetadataPush,
)

if TYPE_CHECKING:
    from ayx_plugin_sdk.core.metadata import Metadata as CoreMetadata
    from ayx_plugin_sdk.providers.amp_provider.resources.generated.metadata_pb2 import (
        Metadata as ProtobufMetadata,
    )


logger = logging.getLogger(__name__)


class OutputMetadataRepository(metaclass=Singleton):
    """Repository that stores output metadata information."""

    _metadata_builder = MetadataBuilder()

    def __init__(self) -> None:
        """Initialize the output metadata repository."""
        self._metadata_map: Dict[str, "CoreMetadata"] = {}

    def save_metadata(self, anchor_name: str, metadata: "CoreMetadata") -> None:
        """Save output metadata information for the assoiciated anchor name."""
        logger.debug(f"Saving metadata {metadata} to anchor {anchor_name}")
        self._metadata_map[anchor_name] = metadata
        logger.debug(f"Current OutputMetadataRepository State: {self._metadata_map}")

        try:
            client = GrpcRepository().get_sdk_engine_client()
        except ValueError:
            pass
        else:
            client.PushOutgoingMetadata(
                OutgoingMetadataPush(
                    output_anchor_name=anchor_name,
                    metadata=self.get_grpc_metadata(anchor_name),
                )
            )

    def get_metadata(self, anchor_name: str) -> "CoreMetadata":
        """Get the output metadata associated with the given anchor name."""
        if anchor_name not in self._metadata_map:
            raise ValueError(f"Anchor {anchor_name} not found in repository.")

        return self._metadata_map[anchor_name]

    def get_grpc_metadata(self, anchor_name: str) -> "ProtobufMetadata":  # type: ignore
        """Get the output Protobuf metadata message associated with the given anchor name."""
        metadata = self.get_metadata(anchor_name)

        return self._metadata_builder.to_protobuf(metadata)

    def delete_metadata(self, anchor_name: str) -> None:
        """Delete the output metadata associated with the given anchor name."""
        if anchor_name not in self._metadata_map:
            raise ValueError(f"Anchor {anchor_name} not found in repository.")
        logger.debug(f"Removing metadata associated with anchor {anchor_name}")
        self._metadata_map.pop(anchor_name)
        logger.debug(f"Current OutputAnchorRepository State: {self._metadata_map}")

    def clear_repository(self) -> None:
        """Delete all data in the repository."""
        logger.debug("Clearing OutputAnchorRepository")
        self._metadata_map = {}
        logger.debug(f"Current OutputAnchorRepository State: {self._metadata_map}")
