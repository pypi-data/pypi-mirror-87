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
"""Proxy Class for managing SDK environment on AMP."""
from typing import TYPE_CHECKING

from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.core.environment_base import EnvironmentBase
from ayx_plugin_sdk.providers.amp_provider.repositories.environment_repository import (
    EnvironmentRepository,
)

if TYPE_CHECKING:
    from ayx_plugin_sdk.core.environment_base import UpdateMode, Locale
    from pathlib import Path


@inherit_docs
class AMPEnvironment(EnvironmentBase):
    """Environment variables for Designer, AMP."""

    @property
    def update_only(self) -> bool:  # noqa: D102
        return EnvironmentRepository().get_update_only()

    @property
    def update_mode(self) -> "UpdateMode":  # noqa: D102
        return EnvironmentRepository().get_update_mode()

    @property
    def designer_version(self) -> str:  # noqa: D102
        return EnvironmentRepository().get_designer_version()

    @property
    def workflow_dir(self) -> "Path":  # noqa: D102
        return EnvironmentRepository().get_workflow_dir()

    @property
    def alteryx_install_dir(self) -> "Path":  # noqa: D102
        return EnvironmentRepository().get_alteryx_install_dir()

    @property
    def alteryx_locale(self) -> "Locale":  # noqa: D102
        return EnvironmentRepository().get_alteryx_locale()

    @property
    def tool_id(self) -> int:  # noqa: D102
        return EnvironmentRepository().get_tool_id()

    def update_tool_config(self, new_config: dict) -> None:  # noqa: D102
        EnvironmentRepository().save_tool_config(new_config)
