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
"""AMP SDK Provider Class."""
import logging
import os
import sys
from logging import Logger
from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING

from ayx_plugin_sdk.core import ProviderBase
from ayx_plugin_sdk.core.doc_utilities import inherit_docs
from ayx_plugin_sdk.providers.amp_provider import AMPDriver
from ayx_plugin_sdk.providers.amp_provider.amp_environment import AMPEnvironment
from ayx_plugin_sdk.providers.amp_provider.amp_io import AMPIO
from ayx_plugin_sdk.providers.amp_provider.repositories.input_anchor_repository import (
    InputAnchorRepository,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.output_anchor_repository import (
    OutputAnchorRepository,
)
from ayx_plugin_sdk.providers.amp_provider.repositories.tool_config_repository import (
    ToolConfigRepository,
)

if TYPE_CHECKING:
    from ayx_plugin_sdk.providers.amp_provider.amp_input_anchor import AMPInputAnchor
    from ayx_plugin_sdk.providers.amp_provider.amp_output_anchor import AMPOutputAnchor


@inherit_docs
class AMPProvider(ProviderBase):
    """Class that provides resources to plugins run with the AMP provider."""

    def __init__(self) -> None:
        """Initialize the AMP resource provider."""
        self.__environment: "AMPEnvironment" = AMPEnvironment()
        self.__io: "AMPIO" = AMPIO()

        self.__logger_name: Optional[str] = None

    def _configure_logging(self) -> None:
        log_directory = (
            Path(os.environ["localappdata"]) / "Alteryx"
            if sys.platform == "win32"
            else Path.home() / ".Alteryx"
        ) / "Log"
        log_directory.mkdir(parents=True, exist_ok=True)
        log_file = log_directory / f"{self.__logger_name}.log"

        logger = logging.getLogger(self.__logger_name)
        handler = logging.FileHandler(log_file)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    @property
    def logger(self) -> "Logger":  # noqa: D102
        if self.__logger_name is None:
            plugin_name: str = AMPDriver().plugin.__class__.__name__
            self.__logger_name = f"{plugin_name}.{self.__environment.tool_id}"
            self._configure_logging()
        return logging.getLogger(self.__logger_name)

    @property
    def io(self) -> "AMPIO":  # noqa: D102
        return self.__io

    @property
    def environment(self) -> "AMPEnvironment":  # noqa: D102
        return self.__environment

    def get_input_anchor(self, name: str) -> "AMPInputAnchor":  # noqa: D102
        return InputAnchorRepository().get_anchor(name)

    def get_output_anchor(self, name: str) -> "AMPOutputAnchor":  # noqa: D102
        return OutputAnchorRepository().get_anchor(name)

    @property
    def tool_config(self) -> Dict:  # noqa: D102
        return ToolConfigRepository().get_tool_config()
