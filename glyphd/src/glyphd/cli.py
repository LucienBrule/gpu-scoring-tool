"""
Command-line interface for glyphd.
"""

import json
import os
import sys
from pathlib import Path

import click
import uvicorn
from fastapi.openapi.utils import get_openapi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


def get_db_path(db_path: str = None) -> str:
    """
    Get the database path from the provided argument, environment variable, or use default.

    Args:
        db_path: Path to the SQLite database file (optional)

    Returns:
        str: Path to the SQLite database file
    """
    if db_path:
        return db_path

    return os.environ.get("GLYPHD_DB_PATH", "data/gpu.db")


@cli.command()
@click.option(
    "--db-path",
    "-d",
    help="Path to the SQLite database file",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force initialization even if the database already exists",
)
def init_db(db_path: str, force: bool):
    """Initialize the SQLite database with the schema.

    This command creates the database file and initializes it with the schema.
    If the database file already exists, it will be overwritten if --force is specified.
    """
    db_path = get_db_path(db_path)
    db_file = Path(db_path)

    # Create the directory if it doesn't exist
    db_file.parent.mkdir(parents=True, exist_ok=True)

    # Check if the database file already exists
    if db_file.exists() and not force:
        click.echo(f"Database file {db_path} already exists. Use --force to overwrite.")
        sys.exit(1)

    # Create the database
    from glyphd.sqlite.models import Base, SchemaVersion

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)

    # Create a session and insert initial schema version
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if schema_version table exists and has records
    if session.query(SchemaVersion).count() == 0:
        # Insert initial schema version
        schema_version = SchemaVersion(
            version="1.0.0",
            description="Initial schema creation",
        )
        session.add(schema_version)
        session.commit()

    click.echo(f"Database initialized at {db_path}")


if __name__ == "__main__":
    cli()
