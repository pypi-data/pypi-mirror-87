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
"""Entrypoint for the test harness."""
from pathlib import Path

from ayx_plugin_sdk.core import Field, FieldType, Metadata
from ayx_plugin_sdk.test_harness.plugin_runner import PluginRunner, RunMode

import pandas as pd

import typer

pd.set_option("display.max_columns", None)

app = typer.Typer()


@app.command()
def version() -> None:
    """Get the version pf the test harness."""
    typer.echo("Version: 1.0.0")


@app.command()
def run_plugin(
    plugin_path: Path = typer.Argument(
        ..., help="The path to the plugin PYZ file to run."
    ),
    tool_name: str = typer.Argument(..., help="The name of the tool to run."),
    run_mode: RunMode = RunMode.full_run,
) -> None:
    """Run a plugin out of process and run data through it."""
    typer.echo(
        f"Running {plugin_path} in {'update only' if run_mode == RunMode.update_only else 'full run'} mode.\n"
    )

    input_data = pd.DataFrame(
        {
            "bool": [True],
            "byte": [5],
            "int16": [10101],
            "int32": [42],
            "int64": [42],
            "fixeddecimal": [
                "Hello World".encode("utf-8")
            ],  # TODO: Implement parsing for fixed decimals, right now they are blobs
            "float": [42.42],
            "double": [42.42],
            "string": ["Hello"],
            "wstring": ["World"],
            "v_string": ["Hello"],
            "v_wstring": ["World"],
            "date": ["2020-09-14"],
            "time": [123],
            "datetime": ["2020-08-28 12:26:42"],
            "blob": ["Hello World".encode("utf-8")],
            "spatialobj": ["Hello World".encode("utf-8")],
        }
    )
    column_names = list(input_data)

    fields = []
    for name in column_names:
        size = 0
        if "string" in name.lower():
            size = 10000

        field_type = FieldType(name)

        fields += [Field(name=name, field_type=field_type, size=size)]

    input_metadata = Metadata(fields)

    runner = PluginRunner(plugin_path, tool_name, input_metadata, input_data)
    runner.run_plugin(run_mode)

    output_metadata = runner.get_output_metadata()
    typer.echo(f"Output metadata is:\n{output_metadata}\n")

    if run_mode == RunMode.full_run:
        output_data = runner.get_output_data()
        typer.echo(f"Output data is:\n{output_data}\n")


def main() -> None:
    """Run the main CLI for the test harness."""
    app()


if __name__ == "__main__":
    main()
