from typer.testing import CliRunner

from savvihub.savvihub_cli import __version__
from savvihub.savvihub_cli import DEFAULT_CONFIG_PATH
from savvihub.common.utils import get_token_from_config

from savvihub.savvihub_cli.main import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"Savvihub CLI Version: {__version__}" in result.stdout


def test_ping():
    result = runner.invoke(app, ["ping"])
    assert result.exit_code == 0
    assert "Response code: 200" in result.stdout
    assert "Response text: pong" in result.stdout


def test_init():
    token_input = "abcd"
    result = runner.invoke(app, ["init"], input=token_input)
    assert result.exit_code == 0
    assert f"Token successfully saved in {DEFAULT_CONFIG_PATH}" in result.stdout

    token_output = get_token_from_config(DEFAULT_CONFIG_PATH)
    assert token_input == token_output
