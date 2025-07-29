from glyphd.cli import cli


def test_cli_exists():
    """Test that the CLI is properly defined."""
    assert cli is not None


def test_serve_command_help(runner):
    """Test that the serve command help text is displayed correctly."""
    result = runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0
    assert "Run the FastAPI server with uvicorn" in result.output


def test_serve_command_parameters(runner):
    """Test that the serve command accepts the expected parameters."""
    # This test doesn't actually start the server, just checks the CLI parsing
    # We use the --help flag to prevent the server from starting
    result = runner.invoke(cli, ["serve", "--help"])
    assert result.exit_code == 0
    assert "--host" in result.output
    assert "--port" in result.output
