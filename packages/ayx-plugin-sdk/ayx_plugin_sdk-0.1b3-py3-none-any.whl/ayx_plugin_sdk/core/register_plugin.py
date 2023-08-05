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
"""Function definition for registering a plugin with the SDK."""
import sys
from typing import Literal, Optional, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ayx_plugin_sdk.core.plugin import Plugin  # noqa: F401
    from ayx_plugin_sdk.providers.e1_provider.e1_plugin_proxy import (  # noqa: F401
        E1PluginProxy,
    )

_ProviderTypes = Literal["e1", "e2", "file"]


def register_plugin(plugin_class: Type["Plugin"]) -> Optional[Type["E1PluginProxy"]]:
    """
    Register a plugin with the SDK.

    The return value of this function should be assigned to a variable
    called AyxPlugin in the entrypoint to the tool in order for the
    E1 Python SDK to properly recognize it.
    """
    # TODO: Add v2 registration
    return {"e1": register_e1_plugin, "file": register_file_provider_plugin}[
        _get_provider()
    ](plugin_class)


def register_e1_plugin(user_plugin_class: Type["Plugin"]) -> Type["E1PluginProxy"]:
    """Register a plugin with the E1 SDK Provider."""
    # This makes a copy of the plugin proxy class. This is an unfortunate requirement
    # given the state of the existing python SDK since the environment shares an
    # interpreter. Without making a copy of the plugin proxy class on registration
    # the stateful property setting of user_plugin_class would be overwritten each
    # time a plugin loads and calls register_e1_plugin, since the library is only
    # loaded into memory once.
    from ayx_plugin_sdk.providers.e1_provider.e1_plugin_proxy import (  # noqa: F811
        E1PluginProxy,
    )

    class ProxyPluginCopy(E1PluginProxy):
        pass

    ProxyPluginCopy.user_plugin_class = user_plugin_class

    return ProxyPluginCopy


def register_file_provider_plugin(user_plugin_class: Type["Plugin"]) -> None:
    """Register a plugin with the File Provider."""
    import ayx_plugin_sdk.providers.file_provider.file_provider as ayx_file_provider

    ayx_file_provider.user_plugin_class = user_plugin_class
    return None


def _get_provider() -> _ProviderTypes:
    if "AlteryxEngineCmd.exe" in sys.executable:
        return "e1"

    # For now, assume if it's not the e1 provider, then it's the file provider
    return "file"
