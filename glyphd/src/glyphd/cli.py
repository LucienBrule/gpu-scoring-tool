"""
Command-line interface for glyphd.
"""
import click
import uvicorn
from typing import Optional

@click.group()
def cli():
    """GlyphD: FastAPI daemon for GPU scoring tool."""
    pass

@cli.command()
@click.option("--host", default="127.0.0.1", help="Host to bind the server to.")
@click.option("--port", default=8000, type=int, help="Port to bind the server to.")
@click.option("--reload", is_flag=True, help="Enable auto-reload for development.")
def serve(host: str, port: int, reload: bool):
    """Run the FastAPI server with uvicorn."""
    click.echo(f"Starting server on {host}:{port}")

    # Import here to avoid circular imports
    from glyphd.api.router import create_app

    app = create_app()
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
    )

if __name__ == "__main__":
    cli()
