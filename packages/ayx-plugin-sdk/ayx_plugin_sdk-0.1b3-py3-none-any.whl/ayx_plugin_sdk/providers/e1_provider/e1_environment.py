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
"""Proxy Class for managing SDK Environment."""
import os
from pathlib import Path
from typing import TYPE_CHECKING

import AlteryxPythonSDK as Sdk

from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.core.environment_base import EnvironmentBase, Locale, UpdateMode


import xmltodict


if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.e1_provider.e1_plugin_proxy import E1PluginProxy


@inherit_docs
class E1Environment(EnvironmentBase):
    """Environment variables for Designer."""

    __slots__ = ["_engine", "_tool_id", "_plugin_proxy"]

    def __init__(
        self, engine: Sdk.AlteryxEngine, tool_id: int, plugin_proxy: "E1PluginProxy"
    ) -> None:
        """Instantiate the Designer environment information."""
        self._engine = engine
        self._tool_id = tool_id
        self._plugin_proxy = plugin_proxy

    @property
    def update_only(self) -> bool:  # noqa: D102
        return bool(self._engine.get_init_var(self._tool_id, "UpdateOnly") == "True")

    @property
    def update_mode(self) -> UpdateMode:  # noqa: D102
        return UpdateMode(self._engine.get_init_var(self._tool_id, "UpdateMode"))

    @property
    def designer_version(self) -> str:  # noqa: D102
        return str(self._engine.get_init_var(self._tool_id, "Version"))

    @property
    def workflow_dir(self) -> Path:  # noqa: D102
        return Path(self._engine.get_init_var(self._tool_id, "DefaultDir"))

    @property
    def alteryx_install_dir(self) -> Path:  # noqa: D102
        return (
            Path(self._engine.get_init_var(self._tool_id, "RuntimeDataPath"))
            .resolve()
            .parent.parent
        )

    @property
    def alteryx_locale(self) -> Locale:  # noqa: D102
        designer_version = self.designer_version[0:6]
        user_settings_path = (
            Path(os.environ["APPDATA"])
            / "Alteryx"
            / "Engine"
            / designer_version
            / "UserSettings.xml"
        )

        with open(user_settings_path) as f:
            user_settings = xmltodict.parse(f.read())
            locale: Locale = user_settings["AlteryxSettings"]["GloablSettings"][
                "HelpLanguage"
            ]["#text"]
            return locale

    @property
    def tool_id(self) -> int:  # noqa: D102
        return self._tool_id

    def update_tool_config(self, new_config: dict) -> None:  # noqa: D102
        if self._plugin_proxy.workflow_config.original_data != new_config:
            self._engine.output_message(
                self._tool_id,
                Sdk.Status.update_output_config_xml,
                xmltodict.unparse({"Configuration": new_config}),
            )
