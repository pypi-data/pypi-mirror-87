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
"""Alteryx Python SDK - Main program."""
import importlib.util
import json
import os
import tempfile
import uuid
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional

from ayx_plugin_sdk.cli.utilities import environment_requires_update, get_alteryx_path
from ayx_plugin_sdk.cli.workspace import Workspace, WorkspaceError
from ayx_plugin_sdk.cli.yxi_installer import YxiInstaller
from ayx_plugin_sdk.providers.file_provider.file_provider import FileProvider
from ayx_plugin_sdk.providers.file_provider.tool_input import ToolInput

import typer

app = typer.Typer(
    help="Run a tool using file inputs and outputs in a pure Python environment."
)


class TemplateToolTypes(str, Enum):
    """Installation Type of Designer."""

    Input = "input"
    MultipleInputs = "multiple-inputs"
    MultipleOutputs = "multiple-outputs"
    Optional = "optional"
    Output = "output"
    Passthrough = "passthrough"
    MultipleInputConnections = "multianchor"
    Doubler = "doubler"


name_to_tool = {
    TemplateToolTypes.Input: "AyxSdkInput",
    TemplateToolTypes.MultipleInputs: "AyxSdkMultipleInputAnchors",
    TemplateToolTypes.MultipleOutputs: "AyxSdkMultiConnectionsMultiOutputAnchor",
    TemplateToolTypes.Optional: "AyxSdkOptionalInputAnchor",
    TemplateToolTypes.Output: "AyxSdkOutput",
    TemplateToolTypes.Passthrough: "AyxSdkPassThrough",
    TemplateToolTypes.MultipleInputConnections: "AyxSdkMultiConnectionsMultiOutputAnchor",
    TemplateToolTypes.Doubler: "AyxSdkDoubler",
}


@app.command()
def run_tool_with_file_provider(
    tool: str = typer.Option(
        ...,
        help="JSON file that specifies the input and output information needed for the file provider to run",
    ),
) -> None:
    """
    Run a tool using file inputs and outputs in a pure Python environment.

    Parameters
    ----------
    tool
        Specifies the path to the JSON file that contains the tool plugin, configuration files, input files, and output files.
    """
    try:
        with open(tool) as fd:
            json_dict = json.load(fd)
    except FileNotFoundError:
        raise RuntimeError(f"Couldn't find tool information file {tool}.")

    tool_input = ToolInput(**json_dict)
    tool_classname = tool_input.tool.plugin
    tool_path = Path(tool_input.tool.path)

    file_provider = FileProvider(
        tool_input.tool_config,
        tool_input.workflow_config,
        inputs=tool_input.inputs or [],
        outputs=tool_input.outputs or [],
        update_tool_config=tool_input.update_tool_config,
    )

    tool_class = _load_user_plugin_class(tool_classname, tool_path)

    # Initialize and run the plugin
    plugin = tool_class(file_provider)
    for input_anchor in file_provider.input_anchors:
        for input_anchor_connection in input_anchor.connections:
            plugin.on_input_connection_opened(input_anchor_connection)
            # TODO Support multiple calls to on_record_packet
            plugin.on_record_packet(input_anchor_connection)
    plugin.on_complete()


def _load_user_plugin_class(tool_classname: str, tool_path: Path) -> Any:
    """Load the plugin and get a reference to its class."""
    root = Path(__file__).resolve().parent
    tool_full_path = root / tool_path
    os.chdir(tool_full_path)
    spec: Any = importlib.util.spec_from_file_location("main", "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, tool_classname)


def handle_workspace_errors(function: Callable) -> Callable:
    """Handle any workspace errors that occur."""

    @wraps(function)
    def decorator(*args: Any, **kwargs: Any) -> None:
        try:
            function(*args, **kwargs)
        except WorkspaceError as e:
            typer.echo(f"ERROR: {e}")
            raise typer.Exit(code=1)

    return decorator


@app.command()
@handle_workspace_errors
def create_ayx_plugin(
    name: str = typer.Option(
        ..., prompt="Tool Name", help="Name of the tool to create."
    ),
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to put this tool in. "
        "Workspace directory will be created if it doesn't exist.",
    ),
    tool_type: TemplateToolTypes = typer.Option(
        ...,
        prompt="Tool type",
        help=f"The type of tool to create. Must be one of: {', '.join(name_to_tool.keys())}",
    ),
) -> None:
    """Create a new plugin plugin for Alteryx Designer."""
    typer.echo("Creating Alteryx Plugin...")
    example_tool_name = name_to_tool[tool_type]

    workspace = Workspace.build_workspace(workspace_directory, allow_creation=True)
    workspace.add_tool_from_template(name, example_tool_name)

    typer.echo(f"Created new tool in directory: {workspace.workspace_dir / name}")


@app.command()
@handle_workspace_errors
def delete_ayx_plugin(
    name: str = typer.Option(
        ..., prompt="Tool Name", help="Name of the tool to delete."
    ),
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to delete this tool from. ",
    ),
) -> None:
    """Delete the Alteryx Plugin Tool in the workspace."""
    workspace = Workspace.build_workspace(workspace_directory)

    typer.echo(f"Deleting Plugin: {name}")
    workspace.delete_tool(name)
    typer.echo(f"Tool successfully deleted.")


@app.command()
@handle_workspace_errors
def create_yxi(
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to package into a YXI.",
    ),
) -> None:
    """Create a YXI from a tools directory."""
    typer.echo("Creating YXI...")

    workspace = Workspace.build_workspace(workspace_directory)
    typer.echo(f"Creating yxi file: {workspace.yxi_name}")

    output_yxi_path = Path(workspace.yxi_name)
    output_yxi_path = output_yxi_path.with_suffix(".yxi")

    workspace.build_yxi(output_yxi_path)

    typer.echo(f"\n Created YXI file at: {output_yxi_path.resolve()}")


@app.command()
@handle_workspace_errors
def designer_build(
    workspace_directory: Path = typer.Option(
        ...,
        prompt="Workspace directory",
        help="Top level workspace directory to install into Designer.",
    ),
    force: bool = typer.Option(
        False, help="Skip installation of Anaconda environment."
    ),
    clean: bool = typer.Option(default=False, help="Remove previous install."),
    designer_path: Optional[Path] = typer.Option(
        default=None,
        help="Path to Designer install, such as 'C:\\Program Files\\Alteryx'. "
        "This option only needs to be specified when Alteryx is installed in a non-standard location.",
    ),
) -> None:
    """Build the tools into designer."""
    typer.echo("Building tools into Alteryx Designer...")

    workspace = Workspace.build_workspace(workspace_directory)

    if force:
        typer.echo("Force updating virtual environment.")
        update_venv = True
    else:
        update_venv = environment_requires_update(workspace)
        if update_venv:
            typer.echo(
                "Virtual Environment has changed. Updating Anaconda environments."
            )
        else:
            typer.echo("Anaconda environments are up to date.")

    if designer_path is None:
        try:
            designer_path = get_alteryx_path()
        except FileNotFoundError:
            typer.echo(
                "ERROR: Couldn't find Designer installed in a standard location. "
                "Please specify using the --designer-path option."
            )
            raise typer.Exit(code=1)

    with tempfile.TemporaryDirectory() as temporary_yxi_directory:
        yxi_path = Path(temporary_yxi_directory) / f"{uuid.uuid4()}.yxi"
        workspace.build_yxi(yxi_path, package_requirements=update_venv)
        YxiInstaller(
            [yxi_path],
            clean=clean,
            update_venv=update_venv,
            alteryx_path=designer_path,
        ).install_yxi()


@app.command()
def docs() -> None:
    """Open the ayx-plugin-sdk documentation in a browser."""
    import webbrowser

    docs_index_html = Path(os.path.dirname(__file__)) / "docs" / "index.html"
    webbrowser.open_new_tab(str(docs_index_html))


def main() -> None:
    """Define the main Entry point to typer."""
    app()


if __name__ == "__main__":
    main()
