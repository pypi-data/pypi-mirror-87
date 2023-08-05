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
"""Tool configuration builder file."""
from typing import Any, Dict

import xmltodict


class ToolConfigBuilder:
    """Builder class for converting the tool configuration XML to and from a dict."""

    @staticmethod
    def to_xml(config_dict: Dict[str, Any]) -> str:
        """Convert a tool configuration dictionary to the expected XML formatted string."""
        return xmltodict.unparse(
            {"Configuration": config_dict}, short_empty_elements=True
        )

    @staticmethod
    def from_xml(xml_string: str) -> Dict[str, Any]:
        """Convert a tool configuration XML to the expected dictionary."""
        return dict(
            xmltodict.parse(xml_string, strip_whitespace=False)["Configuration"] or {}
        )
