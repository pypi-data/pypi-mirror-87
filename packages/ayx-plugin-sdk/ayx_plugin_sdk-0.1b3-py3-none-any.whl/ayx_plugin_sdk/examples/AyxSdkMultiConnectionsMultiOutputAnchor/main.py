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
"""Example multiple input connection anchor tool."""
from ayx_plugin_sdk.core import (
    InputConnectionBase,
    Plugin,
    ProviderBase,
    register_plugin,
)
from ayx_plugin_sdk.core.exceptions import WorkflowRuntimeError


class AyxSdkMultiConnectionsMultiOutputAnchor(Plugin):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: ProviderBase) -> None:
        """Construct a plugin."""
        self.provider = provider
        self.config = self.provider.tool_config
        self.provider.io.info("Plugin initialized.")

        self.input_anchor = self.provider.get_input_anchor("Input")

        if len(self.input_anchor.connections) > 5:
            raise WorkflowRuntimeError("A maximum of 5 input connections is supported.")

        self.connection_name_to_output_anchor = {
            connection.name: self.provider.get_output_anchor(f"Output{anchor_num}")
            for connection, anchor_num in zip(
                self.input_anchor.connections,
                range(1, len(self.input_anchor.connections) + 1),
            )
        }

    def on_input_connection_opened(self, input_connection: InputConnectionBase) -> None:
        """Initialize the Input Connections of this plugin."""
        self.connection_name_to_output_anchor[input_connection.name].open(
            input_connection.metadata
        )
        input_connection.max_packet_size = 1000
        self.provider.io.info(f"Connection opened: {input_connection.name}")

    def on_record_packet(self, input_connection: InputConnectionBase) -> None:
        """Handle the record packet received through the input connection."""
        self.connection_name_to_output_anchor[input_connection.name].write(
            input_connection.read()
        )

    def on_complete(self) -> None:
        """Create all records."""
        self.provider.io.info("Completed processing records.")


AyxPlugin = register_plugin(AyxSdkMultiConnectionsMultiOutputAnchor)
