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
"""Record packet base class definition."""
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from ayx_plugin_sdk.core.metadata import Metadata
    import pandas as pd


class RecordPacketBase(ABC):
    """Abstract class that describes a record packet."""

    @property
    @abstractmethod
    def metadata(self) -> "Metadata":
        """
        Get the packet metadata.

        Returns
        -------
        Metadata
            The metadata for records contained in the packet.
        """
        raise NotImplementedError()

    @abstractmethod
    def to_dataframe(self) -> "pd.DataFrame":
        """
        Get the packet data as a dataframe.

        Returns
        -------
        pd.DataFrame
            The dataframe containing all records in the packet.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_dataframe(
        cls, metadata: "Metadata", df: "pd.DataFrame"
    ) -> "RecordPacketBase":
        """
        Set the packet data from a dataframe.

        Parameters
        ----------
        metadata
            The metadata for the records.
        df
            The dataframe to generate records from.
        """
        raise NotImplementedError()

    def __eq__(self, other: Any) -> bool:
        """Check equality between two packets."""
        if not isinstance(other, RecordPacketBase):
            return NotImplemented

        if self.metadata != other.metadata:
            return False

        import pandas as pd

        try:
            pd.testing.assert_frame_equal(self.to_dataframe(), other.to_dataframe())
        except AssertionError:
            return False
        else:
            return True

    def __str__(self) -> str:
        """Return the string representation of a record packet."""
        return f"Metadata: {self.metadata}\nDataframe: {self.to_dataframe()}"
