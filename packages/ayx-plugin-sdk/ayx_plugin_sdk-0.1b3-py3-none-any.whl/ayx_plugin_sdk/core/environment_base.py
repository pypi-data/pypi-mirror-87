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
"""Runtime environment information."""
from abc import ABC, abstractmethod
from enum import Enum, unique
from pathlib import Path
from typing import Literal


Locale = Literal["en", "it", "fr", "de", "ja", "es", "pt", "zh"]


@unique
class UpdateMode(Enum):
    """The types of update modes that can run in Alteryx Designer."""

    NO_UPDATE_MODE = ""
    QUICK = "Quick"
    FULL = "Full"


class EnvironmentBase(ABC):
    """
    Environment information class definition.

    This class provides information about the runtime environment
    of the tool that is running, for example, if it is running as update
    only, the version of the system running, etc.
    """

    @property
    @abstractmethod
    def update_only(self) -> bool:
        """
        Check if the engine is running in update only mode.

        Returns
        -------
        bool
            True if running in update only.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def update_mode(self) -> UpdateMode:
        """Get the type of update running."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def designer_version(self) -> str:
        """
        Return the version of Designer that is being used.

        Returns
        -------
        str
            A version in the format of 1.2.3.4

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def workflow_dir(self) -> Path:
        """Get the directory for the currently-running workflow."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def alteryx_install_dir(self) -> Path:
        """Get the Alteryx install directory."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def alteryx_locale(self) -> Locale:
        """Retrieve locale code from Alteryx user settings."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def tool_id(self) -> int:
        """Get the current tool's workflow ID."""
        raise NotImplementedError()

    @abstractmethod
    def update_tool_config(self, new_config: dict) -> None:
        """
        Update the tool's configuration.

        Parameters
        ----------
        new_config
            The new configuration to set for the tool.

        Returns
        -------
        None

        """
        raise NotImplementedError()
