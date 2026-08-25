import os
import pytest
from typer.testing import CliRunner
from pattern_detector.adapters.inbound.cli.main import app

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "DPX-Dart" in result.stdout


def test_cli_catalog():
    result = runner.invoke(app, ["catalog"], env={"COLUMNS": "300"})
    assert result.exit_code == 0
    assert "sealed_class_adt" in result.stdout
    assert "bloc_cubit_state_machine" in result.stdout


def test_cli_scan(tmp_path):
    dart_file = tmp_path / "main.dart"
    dart_file.write_text("""
    import 'package:flutter/material.dart';
    sealed class AppState {}
    class AppWidget extends StatelessWidget {
      @override
      Widget build(BuildContext context) => Container();
    }
    """)

    html_out = tmp_path / "hud.html"
    json_out = tmp_path / "res.json"

    result = runner.invoke(
        app,
        [
            "scan",
            str(tmp_path),
            "--html",
            str(html_out),
            "--json",
            str(json_out),
        ],
    )
    assert result.exit_code == 0
    assert html_out.exists()
    assert json_out.exists()
