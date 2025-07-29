"""
SQLite storage backend for GPU listings.

This module implements a SQLite storage backend for GPU listings using SQLAlchemy Core.
"""

import logging
import os
from datetime import datetime
from typing import List, Optional

from rich.logging import RichHandler
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from glyphd.api.models import GPUListingDTO, ImportMetadata
from glyphd.core.storage.interface import ListingStore

# Configure logging
try:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger("sqlite_store")
except ImportError:
    # Fall back to standard logging if rich is not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("sqlite_store")


class SqliteListingStore(ListingStore):
    """
    SQLite storage backend for GPU listings.

    This class implements the ListingStore interface using SQLite as the storage backend.
    It uses SQLAlchemy Core to interact with the database.
    """

    def __init__(self, db_path: str):
        """
        Initialize the SQLite storage backend.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.engine = self._create_engine()
        self._ensure_schema()

    def _create_engine(self) -> Engine:
        """
        Create a SQLAlchemy engine for the SQLite database.

        Returns:
            A SQLAlchemy engine
        """
        # Create the directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Create the engine
        engine = create_engine(f"sqlite:///{self.db_path}")
        logger.info(f"Connected to SQLite database at {self.db_path}")
        return engine

    def _ensure_schema(self) -> None:
        """
        Ensure that the database schema exists.

        If the database is empty, this method will create the schema.
        """
        # Check if the schema_version table exists
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"))
            if result.fetchone() is None:
                logger.info("Schema not found, initializing database...")
                self._initialize_schema()
            else:
                logger.info("Schema already exists")

    def _initialize_schema(self) -> None:
        """
        Initialize the database schema.

        This method reads the schema.sql file and executes it to create the database schema.
        """
        # Read the schema.sql file using importlib.resources
        from importlib.resources import files

        schema_path = files("glyphd.resources.sql").joinpath("schema.sql")
        schema_sql = schema_path.read_text(encoding="utf-8")

        # Execute the schema SQL directly using SQLite's executescript
        # This bypasses SQLAlchemy's statement preparation and allows SQLite to handle
        # the script natively, including triggers with BEGIN...END blocks
        with self.engine.connect() as conn:
            # Enable foreign keys
            conn.execute(text("PRAGMA foreign_keys = ON"))

            # Use raw connection to execute the script
            raw_conn = conn.connection
            raw_conn.executescript(schema_sql)

            conn.commit()
            logger.info("Schema initialized successfully")

    def insert_listings(self, listings: List[GPUListingDTO], import_id: str) -> int:
        """
        Insert a batch of listings into the store with the given import ID.

        If listings with the same import ID already exist, they will be replaced.

        Args:
            listings: The listings to insert
            import_id: The ID of the import batch

        Returns:
            The number of listings inserted
        """
        if not listings:
            logger.warning("No listings to insert")
            return 0

        # Create or update the import batch and insert the listings
        with self.engine.connect() as conn:
            # Check if the import batch already exists
            result = conn.execute(
                text("SELECT import_id FROM import_batches WHERE import_id = :import_id"),
                {"import_id": import_id},
            )
            if result.fetchone() is None:
                # Create the import batch
                conn.execute(
                    text(
                        """
                        INSERT INTO import_batches (import_id, source, record_count, description)
                        VALUES (:import_id, :source, :record_count, :description)
                        """
                    ),
                    {
                        "import_id": import_id,
                        "source": "api",
                        "record_count": len(listings),
                        "description": f"Import batch {import_id}",
                    },
                )
                logger.info(f"Created import batch {import_id}")
            else:
                # Update the import batch
                conn.execute(
                    text(
                        """
                        UPDATE import_batches
                        SET record_count = :record_count
                        WHERE import_id = :import_id
                        """
                    ),
                    {"import_id": import_id, "record_count": len(listings)},
                )
                logger.info(f"Updated import batch {import_id}")

                # Delete existing listings with the same import ID to ensure idempotent inserts
                conn.execute(
                    text("DELETE FROM scored_listings WHERE import_id = :import_id"),
                    {"import_id": import_id},
                )
                logger.info(f"Deleted existing listings with import ID {import_id}")

            # Insert the listings
            for listing in listings:
                # Ensure the model exists
                conn.execute(
                    text(
                        """
                        INSERT OR IGNORE INTO models (model, vram_gb, tdp_watts, mig_support, nvlink, import_id)
                        VALUES (:model, :vram_gb, :tdp_watts, :mig_support, :nvlink, :import_id)
                        """
                    ),
                    {
                        "model": listing.canonical_model,
                        "vram_gb": listing.vram_gb,
                        "tdp_watts": listing.tdp_watts,
                        "mig_support": listing.mig_support,
                        "nvlink": 1 if listing.nvlink else 0,
                        "import_id": import_id,
                    },
                )

                # Insert the scored listing
                conn.execute(
                    text(
                        """
                        INSERT INTO scored_listings (
                            canonical_model, price, vram_gb, tdp_watts, mig_support, nvlink, score, import_id
                        )
                        VALUES (
                            :model, :price, :vram_gb, :tdp_watts, :mig_support, :nvlink, :score, :import_id
                        )
                        """
                    ),
                    {
                        "model": listing.canonical_model,
                        "price": listing.price,
                        "vram_gb": listing.vram_gb,
                        "tdp_watts": listing.tdp_watts,
                        "mig_support": listing.mig_support,
                        "nvlink": 1 if listing.nvlink else 0,
                        "score": listing.score,
                        "import_id": import_id,
                    },
                )

            # Commit the transaction
            conn.commit()
            logger.info(f"Inserted {len(listings)} listings with import ID {import_id}")
            return len(listings)

    def query_listings(
        self,
        model: Optional[str] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        region: Optional[str] = None,
        after: Optional[datetime] = None,
    ) -> List[GPUListingDTO]:
        """
        Query listings from the store with optional filters.

        Args:
            model: Filter by canonical model name
            min_score: Filter by minimum score
            max_score: Filter by maximum score
            region: Filter by region
            after: Filter by listings seen after this timestamp

        Returns:
            A list of listings matching the filters
        """
        # Build the query
        query = """
            SELECT canonical_model, price, vram_gb, tdp_watts, mig_support, nvlink, score
            FROM scored_listings
            WHERE 1=1
        """
        params = {}

        # Add filters
        if model:
            query += " AND canonical_model = :model"
            params["model"] = model

        if min_score is not None:
            query += " AND score >= :min_score"
            params["min_score"] = min_score

        if max_score is not None:
            query += " AND score <= :max_score"
            params["max_score"] = max_score

        if region:
            query += " AND region = :region"
            params["region"] = region

        if after:
            query += " AND seen_at >= :after"
            params["after"] = after.isoformat()

        # Execute the query
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()

        # Convert rows to DTOs
        listings = []
        for row in rows:
            listing = GPUListingDTO(
                canonical_model=row[0],
                price=row[1],
                vram_gb=row[2],
                tdp_watts=row[3],
                mig_support=row[4],
                nvlink=bool(row[5]),
                score=row[6],
            )
            listings.append(listing)

        logger.info(f"Found {len(listings)} listings matching the filters")
        return listings

    def list_imports(self) -> List[ImportMetadata]:
        """
        List all import batches in the store.

        Returns:
            A list of import batch metadata
        """
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT import_id, imported_at, source, record_count, description
                    FROM import_batches
                    ORDER BY imported_at DESC
                    """
                )
            )
            rows = result.fetchall()

        # Convert rows to DTOs
        imports = []
        for row in rows:
            import_metadata = ImportMetadata(
                import_id=row[0],
                imported_at=datetime.fromisoformat(row[1]),
                source=row[2],
                record_count=row[3],
                description=row[4],
            )
            imports.append(import_metadata)

        logger.info(f"Found {len(imports)} import batches")
        return imports
