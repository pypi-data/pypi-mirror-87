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
"""Entrypoint for tracer bullet application."""
import logging
import os
from pathlib import Path

from ayx_plugin_sdk.providers.amp_provider.grpc_util import SocketAddress
from ayx_plugin_sdk.providers.amp_provider.repositories.grpc_repository import (
    GrpcRepository,
)
from ayx_plugin_sdk.tracer_bullet.sdk_tool_runner import SdkToolRunner

import typer

app = typer.Typer()

log_dir = Path(os.environ.get("LOCALAPPDATA") or "/temp") / "Alteryx" / "Log"
log_dir.mkdir(parents=True, exist_ok=True)

log_file = log_dir / "TracerBulletSdkToolService.log"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(str(log_file), encoding="utf-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


@app.command()
def version() -> None:
    """Get the version of the CLI."""
    typer.echo("Version 1.0.0")


@app.command()
def start_sdk_tool_service(
    tool_name: str, sdk_engine_server_address: str = "localhost:65000"
) -> None:
    """Start the SDK Tool service."""
    try:
        startup_msg = f"Starting {tool_name} tool with AMP Provider."

        typer.echo(startup_msg)
        logger.info(startup_msg)

        runner = SdkToolRunner(
            SocketAddress.from_address_str(sdk_engine_server_address)
        )

        try:
            runner.start_service()
        except Exception as e:
            err_str = f"ERROR: Couldn't start service."
            typer.echo(err_str)
            logger.error(err_str)
            logger.exception(e)
            raise typer.Exit(code=1)

        success_msg = f"Successfully started python server at {GrpcRepository().get_sdk_tool_server_address().address}."
        typer.echo(success_msg)
        logger.info(success_msg)

        return_status = runner.handshake_with_sdk_engine_service()

        success_msg = f"SDK ENGINE CLIENT: Successfully called into SDK Engine service with response:\n{return_status}"
        typer.echo(success_msg)
        logger.info(success_msg)

        runner.wait_for_termination()
    except Exception as e:
        typer.echo(f"EXCEPTION: {e}")
        logger.exception(e)

        raise


def main() -> None:
    """Entrypoint method for the tracer bullet application."""
    app()


if __name__ == "__main__":
    main()
