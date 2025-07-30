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
from glyphsieve.core.normalization import fuzzy_match

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
        # Read the schema.sql file using ResourceContext
        from glyphd.core.resources.resource_context import GlyphdResourceContext

        resource_context = GlyphdResourceContext()
        schema_sql = resource_context.load_text("sql/schema.sql")

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

            # Insert the listings with sequential import_index
            for import_index, listing in enumerate(listings, start=1):
                # Ensure the model exists
                conn.execute(
                    text(
                        """
                        INSERT OR IGNORE INTO models (
                            model, vram_gb, tdp_watts, mig_support, nvlink, import_id, import_index
                        )
                        VALUES (:model, :vram_gb, :tdp_watts, :mig_support, :nvlink, :import_id, :import_index)
                        """
                    ),
                    {
                        "model": listing.canonical_model,
                        "vram_gb": listing.vram_gb,
                        "tdp_watts": listing.tdp_watts,
                        "mig_support": listing.mig_support,
                        "nvlink": 1 if listing.nvlink else 0,
                        "import_id": import_id,
                        "import_index": import_index,
                    },
                )

                # Insert the scored listing
                conn.execute(
                    text(
                        """
                        INSERT INTO scored_listings (
                            canonical_model, price, vram_gb, tdp_watts, mig_support, nvlink, score,
                            import_id, import_index
                        )
                        VALUES (
                            :model, :price, :vram_gb, :tdp_watts, :mig_support, :nvlink, :score,
                            :import_id, :import_index
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
                        "import_index": import_index,
                    },
                )

            # Commit the transaction
            conn.commit()
            logger.info(f"Inserted {len(listings)} listings with import ID {import_id}")
            return len(listings)

    def _get_fuzzy_matched_models(self, model: str) -> List[str]:
        """
        Get fuzzy matched models for the given model name.

        Args:
            model: Model name to match against

        Returns:
            List of matched model names, empty if no match found
        """
        # Get all unique models from the database for fuzzy matching
        with self.engine.connect() as conn:
            model_result = conn.execute(text("SELECT DISTINCT canonical_model FROM scored_listings"))
            all_models = [row[0] for row in model_result.fetchall()]

        # Create a models dictionary for fuzzy matching (format expected by fuzzy_match)
        models_dict = {m: [m] for m in all_models}

        # Apply fuzzy matching
        matched_model, score = fuzzy_match(model, models_dict, threshold=70.0)
        if matched_model:
            return [matched_model]
        else:
            logger.info(f"No fuzzy match found for model: {model}")
            return []

    def _build_query_with_filters(
        self,
        fuzzy_matched_models: List[str],
        min_price: Optional[float],
        max_price: Optional[float],
        min_score: Optional[float],
        max_score: Optional[float],
        region: Optional[str],
        after: Optional[datetime],
        import_id: Optional[str],
        limit: Optional[int],
        offset: Optional[int],
    ) -> tuple[str, dict]:
        """
        Build SQL query with filters and return query string and parameters.

        Returns:
            Tuple of (query_string, parameters_dict)
        """
        query = """
            SELECT canonical_model, price, vram_gb, tdp_watts, mig_support, nvlink, score, import_id, import_index
            FROM scored_listings
            WHERE 1=1
        """
        params = {}

        # Handle fuzzy matched models
        if fuzzy_matched_models:
            placeholders = ", ".join(f":model_{i}" for i in range(len(fuzzy_matched_models)))
            query += f" AND canonical_model IN ({placeholders})"
            for i, matched_model in enumerate(fuzzy_matched_models):
                params[f"model_{i}"] = matched_model

        # Declarative filter specs
        filter_specs = [
            ("price", ">=", "min_price", min_price),
            ("price", "<=", "max_price", max_price),
            ("score", ">=", "min_score", min_score),
            ("score", "<=", "max_score", max_score),
            ("region", "=", "region", region),
            ("seen_at", ">=", "after", after.isoformat() if after else None),
            ("import_id", "=", "import_id", import_id),
        ]

        for column, op, param_name, value in filter_specs:
            if value is not None:
                query += f" AND {column} {op} :{param_name}"
                params[param_name] = value

        if limit is not None:
            query += " LIMIT :limit"
            params["limit"] = limit

        if offset is not None:
            query += " OFFSET :offset"
            params["offset"] = offset

        return query, params

    def _convert_rows_to_dtos(self, rows) -> List[GPUListingDTO]:
        """
        Convert database rows to GPUListingDTO objects.

        Args:
            rows: Database result rows

        Returns:
            List of GPUListingDTO objects
        """
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
                import_id=row[7],
                import_index=row[8],
            )
            listings.append(listing)
        return listings

    def query_listings(
        self,
        model: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        region: Optional[str] = None,
        after: Optional[datetime] = None,
        import_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[GPUListingDTO]:
        """
        Query listings from the store with optional filters.

        Args:
            model: Filter by canonical model name (supports fuzzy matching)
            min_price: Filter by minimum price
            max_price: Filter by maximum price
            min_score: Filter by minimum score
            max_score: Filter by maximum score
            region: Filter by region
            after: Filter by listings seen after this timestamp
            import_id: Filter by import batch ID
            limit: Maximum number of results to return
            offset: Number of results to skip for pagination

        Returns:
            A list of listings matching the filters
        """
        # Handle fuzzy matching for model if provided
        fuzzy_matched_models = []
        if model:
            fuzzy_matched_models = self._get_fuzzy_matched_models(model)
            if not fuzzy_matched_models:
                return []

        # Build the query with filters
        query, params = self._build_query_with_filters(
            fuzzy_matched_models, min_price, max_price, min_score, max_score, region, after, import_id, limit, offset
        )

        # Execute the query
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()

        # Convert rows to DTOs
        listings = self._convert_rows_to_dtos(rows)

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
