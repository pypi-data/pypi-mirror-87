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
"""Builder file for Output Anchor."""
import logging
import sys
from typing import TYPE_CHECKING

from ayx_plugin_sdk.providers.amp_provider.builders import MetadataBuilder
from ayx_plugin_sdk.providers.amp_provider.resources.generated.outgoing_anchor_pb2 import (
    OutgoingAnchor as ProtobufOutputAnchor,
)

if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider import AMPOutputAnchor


logger = logging.getLogger(__name__)


class OutputAnchorBuilder:
    """Builder class for serializing and deserializing output anchors."""

    @staticmethod
    def from_protobuf(
        protobuf_output_anchor: ProtobufOutputAnchor,
    ) -> "AMPOutputAnchor":
        """Given an AMPOutputAnchor as a protobuf, return its Python object."""
        from ayx_plugin_sdk.providers.amp_provider import AMPOutputAnchor

        logger.debug(
            f"Deserializing Output Anchor {protobuf_output_anchor.name} from protobuf"
        )
        core_output_anchor = AMPOutputAnchor(
            protobuf_output_anchor.name,
            num_connections=protobuf_output_anchor.num_connections or 0,
        )

        if (
            protobuf_output_anchor.options
            != ProtobufOutputAnchor.OutgoingAnchorOptions.ORDERED
        ):
            raise ValueError("Only ordered output anchors are supported.")
        logger.debug(f"Deserialized Output Anchor {core_output_anchor} from protobuf")
        return core_output_anchor

    @staticmethod
    def to_protobuf(
        output_anchor: "AMPOutputAnchor",
        anchor_options: ProtobufOutputAnchor.OutgoingAnchorOptions = ProtobufOutputAnchor.OutgoingAnchorOptions.ORDERED,
        record_limit: int = sys.maxsize,
    ) -> ProtobufOutputAnchor:
        """Given an AMPOutputAnchor, return a protobuf representation."""
        metadata = (
            MetadataBuilder.to_protobuf(output_anchor.metadata)
            if output_anchor.is_open
            else None
        )
        logger.debug(f"Serialized metadata {metadata} to protobuf")
        protobuf_output_anchor = ProtobufOutputAnchor(
            name=output_anchor.name,
            num_connections=output_anchor.num_connections,
            metadata=metadata,
            options=anchor_options,
            record_limit=record_limit,
        )
        logger.debug(f"Serialized Ouptut Anchor {output_anchor.name} to protobuf")
        return protobuf_output_anchor
