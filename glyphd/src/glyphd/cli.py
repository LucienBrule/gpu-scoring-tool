"""
Command-line interface for glyphd.
"""

import json
import os

import click
import uvicorn
from fastapi.openapi.utils import get_openapi


@click.group()
def cli():
    """GlyphD: FastAPI daemon for GPU scoring tool."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind the server to.")
@click.option("--port", default=8080, type=int, help="Port to bind the server to.")
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


@cli.command()
@click.argument("output_path", type=click.Path(), default="openapi.json")
def export_openapi(output_path: str):
    """Export the OpenAPI schema to a JSON file.

    Args:
        output_path: Path where the OpenAPI schema will be saved.
    """
    # Import here to avoid circular imports
    from glyphd.api.router import create_app

    click.echo(f"Generating OpenAPI schema to {output_path}")

    # Create the FastAPI app (without serving)
    app = create_app()

    # Get the OpenAPI schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Write the schema to the output file
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)

    click.echo(f"✅ OpenAPI schema exported to {output_path}")


if __name__ == "__main__":
    cli()
