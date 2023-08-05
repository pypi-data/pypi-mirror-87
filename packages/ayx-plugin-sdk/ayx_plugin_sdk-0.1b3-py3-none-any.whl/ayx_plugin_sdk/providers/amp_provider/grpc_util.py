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
"""Functions demonstrating available port finding for server binding/client connection."""
import copy
from concurrent import futures

from ayx_plugin_sdk.providers.amp_provider.resources.generated.sdk_engine_service_pb2_grpc import (
    SdkEngineStub,
)
from ayx_plugin_sdk.providers.amp_provider.resources.generated.sdk_tool_service_pb2_grpc import (
    add_SdkToolServicer_to_server,
)
from ayx_plugin_sdk.tracer_bullet.sdk_tool_service import SdkToolService

import grpc


def build_sdk_tool_server(sdk_tool_address: "SocketAddress"):  # type: ignore
    """Build the sdk tool server."""
    sdk_tool_address = copy.deepcopy(sdk_tool_address)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SdkToolServicer_to_server(SdkToolService(), server)  # type: ignore
    sdk_tool_address.port = server.add_insecure_port(sdk_tool_address.address)

    return server, sdk_tool_address


def build_sdk_engine_client(sdk_engine_address: "SocketAddress") -> SdkEngineStub:
    """Build the SDK engine client."""
    channel = grpc.insecure_channel(sdk_engine_address.address)
    client = SdkEngineStub(channel)  # type: ignore
    return client  # type: ignore


class SocketAddress:
    """Class for tracking host and port information."""

    @classmethod
    def from_address_str(cls, address_str: str) -> "SocketAddress":
        """Construct a socket address from an address string."""
        host, port = address_str.split(":")
        return cls(host, int(port))

    def __init__(self, host: str, port: int) -> None:
        """Construct a socket address."""
        self.host = host
        self.port = port

    @property
    def address(self) -> str:
        """Get the address string containing both host and port."""
        return f"{self.host}:{self.port}"
