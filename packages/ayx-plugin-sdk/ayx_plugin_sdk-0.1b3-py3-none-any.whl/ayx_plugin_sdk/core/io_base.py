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
"""IO utility functions for reading/writing to Alteryx Designer."""
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from pathlib import Path


class IoBase(ABC):
    """IO base class."""

    @abstractmethod
    def error(self, error_msg: str) -> None:
        """
        Display an error message in the Results window.

        Parameters
        ----------
        error_msg
            A string to show as an error in the Alteryx Designer Results panel.
        """
        raise NotImplementedError()

    @abstractmethod
    def warn(self, warn_msg: str) -> None:
        """
        Display a warning message in the Results window.

        Parameters
        ----------
        warn_msg
            A string to show as a warning in the Alteryx Designer Results panel.
        """
        raise NotImplementedError()

    @abstractmethod
    def info(self, info_msg: str) -> None:
        """
        Display an info message in the Results window.

        Parameters
        ----------
        info_msg
            A string to show as an info message in the Alteryx Designer Results panel.
        """
        raise NotImplementedError()

    @abstractmethod
    def translate_msg(self, msg: str, *args: Any) -> str:
        """
        Translate a message to the current locale.

        .. deprecated:: 0.1.0a
          `translate_msg` is not the recommended translation mechanism. See
          the documentation on localization.

        Parameters
        ----------
        msg
            A string to translate.
        args
            Arguments for string interpolation.
        """
        raise NotImplementedError()

    @abstractmethod
    def update_progress(self, percent: float) -> None:
        """
        Update tool progress.

        Parameters
        ----------
        percent
            A number between 0 and 100 to indicate the progress percent.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_temp_file(self, extension: str = "tmp", options: int = 0) -> "Path":
        """
        Create a temporary file managed by Designer.

        Parameters
        ----------
        extension
            The extension of the new file.
        options
            Lifecycle management options for the temp file.

            0: A normal temp file. It is cleaned up by Designer when a Run completes.

            1: A temp file for a GUI element, like a browse, that the GUI is responsible for cleaning up.

            2: A temp file for a GUI element, like a browse, that the GUI is responsible for cleaning up.
            Additionally, the file name is not made to be unique.
            Use when the extension argument already contains a unique ID.

        Returns
        -------
        Path
            Path to the new temp file.
        """
        raise NotImplementedError()

    @abstractmethod
    def decrypt_password(self, password: str) -> str:
        """
        Decrypt password.

        Parameters
        ----------
        password
            Password to decrypt.

        Returns
        -------
        str
            Decrypted password.
        """
        raise NotImplementedError()
