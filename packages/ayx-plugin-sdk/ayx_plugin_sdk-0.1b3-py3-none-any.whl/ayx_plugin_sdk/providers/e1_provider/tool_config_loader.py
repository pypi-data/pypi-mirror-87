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
"""Tool configuration loader definition."""
import os
import sys
from pathlib import Path
from typing import Any, Dict

import xmltodict


class ToolConfigLoader:
    """Tool configuration loader definition."""

    def __init__(self, tool_name: str):
        """Construct a tool configuration loader."""
        self.tool_name = tool_name

    def get_tool_config(self) -> Dict[str, Any]:
        """Get the tool config of this tool from its config.xml file."""
        try:
            with open(str(self.get_tool_config_filepath())) as fd:
                tool_config = dict(xmltodict.parse(fd.read(), strip_whitespace=False))
        except FileNotFoundError:
            raise RuntimeError(f"Couldn't find tool with name {self.tool_name}.")
        else:
            return tool_config

    def get_tool_config_filepath(self) -> Path:
        """Get the path to the tool configuration file."""
        return Path(
            os.path.join(str(self.get_tool_path()), f"{self.tool_name}Config.xml")
        )

    def get_tool_path(self) -> Path:
        """Get the path to the directory containing the current tool's definition."""
        return Path(os.path.join(str(self.get_tools_location()), self.tool_name))

    def get_tools_location(self) -> Path:
        """Get the location of Alteryx tools that contain the current tool."""
        tools_rel_path = Path("Alteryx/Tools")
        admin_path = Path(os.environ["ALLUSERSPROFILE"]) / tools_rel_path
        user_path = Path(os.environ["APPDATA"]) / tools_rel_path

        alteryx_bin = (
            Path(os.path.dirname(sys.executable))
            if "AlteryxEngineCmd.exe" in sys.executable
            else Path("")
        )
        html_plugins_path = alteryx_bin / "HtmlPlugins"

        for path in user_path, admin_path, html_plugins_path:
            if path.is_dir() and self.tool_name in [
                child_dir.name for child_dir in path.iterdir()
            ]:
                return path

        raise RuntimeError("Tool is not located in Alteryx install locations.")
