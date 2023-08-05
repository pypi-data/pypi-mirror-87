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
"""Alteryx Python SDK - File Adapter for standalone testing."""

from .file_adapter import FileAdapter
from .file_provider import FileProvider
from .file_provider_input_anchor import FileProviderInputAnchor
from .file_provider_input_connection import FileProviderInputConnection
from .file_provider_output_anchor import FileProviderOutputAnchor
from .tool_input import AnchorDefinition, ToolDefinition, ToolInput

__all__ = [
    "AnchorDefinition",
    "FileAdapter",
    "FileProvider",
    "FileProviderInputAnchor",
    "FileProviderInputConnection",
    "FileProviderOutputAnchor",
    "ToolDefinition",
    "ToolInput",
]
