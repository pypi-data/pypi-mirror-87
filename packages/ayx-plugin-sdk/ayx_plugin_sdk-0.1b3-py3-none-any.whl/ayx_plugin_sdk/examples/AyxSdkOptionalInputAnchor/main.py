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
"""Example optional input anchor tool."""
from ayx_plugin_sdk.core import (
    FieldType,
    InputConnectionBase,
    Metadata,
    Plugin,
    ProviderBase,
    RecordPacket,
    register_plugin,
)


class AyxSdkOptionalInputAnchor(Plugin):
    """Concrete implementation of an AyxPlugin."""

    def __init__(self, provider: ProviderBase) -> None:
        """Construct a plugin."""
        self.provider = provider
        self.tool_config = provider.tool_config
        self.config_value = self.tool_config["Value"]
        self.output_anchor = self.provider.get_output_anchor("Output")
        self.input_anchor = self.provider.get_input_anchor("Input")
        self.provider.io.info("Plugin initialized.")

    def on_input_connection_opened(self, input_connection: InputConnectionBase) -> None:
        """Initialize the Input Connections of this plugin."""
        if not self.output_anchor.is_open:
            self.output_anchor.open(input_connection.metadata)

    def on_record_packet(self, input_connection: InputConnectionBase) -> None:
        """Handle the record packet received through the input connection."""
        self.provider.io.info("Record packet received!")
        self.output_anchor.write(input_connection.read())

    def on_complete(self) -> None:
        """Create all records."""
        if not self.input_anchor.connections:
            output_metadata = Metadata()
            output_metadata.add_field("OptionalField", FieldType.float)
            self.output_anchor.open(output_metadata)
            import pandas as pd

            df = pd.DataFrame({"OptionalField": [self.config_value]})
            packet = RecordPacket.from_dataframe(output_metadata, df)
            self.output_anchor.write(packet)

        self.provider.io.info("Completed processing records.")


AyxPlugin = register_plugin(AyxSdkOptionalInputAnchor)
