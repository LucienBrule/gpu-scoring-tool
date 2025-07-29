"""Initial schema creation

Revision ID: 20250729_initial
Revises:
Create Date: 2025-07-29 11:15:00.000000

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20250729_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Enable foreign key constraints
    op.execute("PRAGMA foreign_keys = ON")

    # Schema version tracking
    op.create_table(
        "schema_version",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("applied_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Insert initial schema version
    op.execute("INSERT INTO schema_version (version, description) VALUES ('1.0.0', 'Initial schema creation')")

    # Import batch tracking for differential updates
    op.create_table(
        "import_batches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("import_id", sa.String(), nullable=False),
        sa.Column("imported_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("record_count", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("import_id"),
    )

    # GPU Models table
    op.create_table(
        "models",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("vram_gb", sa.Integer(), nullable=True),
        sa.Column("tdp_watts", sa.Integer(), nullable=True),
        sa.Column("mig_support", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("nvlink", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("generation", sa.String(), nullable=True),
        sa.Column("cuda_cores", sa.Integer(), nullable=True),
        sa.Column("slot_width", sa.Integer(), nullable=True),
        sa.Column("pcie_generation", sa.Integer(), nullable=True),
        sa.Column("listing_count", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("min_price", sa.Float(), nullable=True),
        sa.Column("median_price", sa.Float(), nullable=True),
        sa.Column("max_price", sa.Float(), nullable=True),
        sa.Column("avg_price", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("import_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["import_id"], ["import_batches.import_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model"),
    )

    # Create index on model name for faster lookups
    op.create_index("idx_models_model", "models", ["model"], unique=False)

    # Raw Listings table
    op.create_table(
        "listings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("canonical_model", sa.String(), nullable=False),
        sa.Column("match_type", sa.String(), nullable=False),
        sa.Column("match_score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("import_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["canonical_model"], ["models.model"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["import_id"], ["import_batches.import_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for faster lookups
    op.create_index("idx_listings_canonical_model", "listings", ["canonical_model"], unique=False)
    op.create_index("idx_listings_import_id", "listings", ["import_id"], unique=False)

    # Scored Listings table
    op.create_table(
        "scored_listings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("canonical_model", sa.String(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("vram_gb", sa.Integer(), nullable=False),
        sa.Column("tdp_watts", sa.Integer(), nullable=False),
        sa.Column("mig_support", sa.Integer(), nullable=True, server_default=sa.text("0")),
        sa.Column("nvlink", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("generation", sa.String(), nullable=True),
        sa.Column("cuda_cores", sa.Integer(), nullable=True),
        sa.Column("slot_width", sa.Integer(), nullable=True),
        sa.Column("pcie_generation", sa.Integer(), nullable=True),
        sa.Column("form_factor", sa.String(), nullable=True, server_default=sa.text("'Standard'")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("warnings", sa.Text(), nullable=True),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("condition", sa.String(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("min_order_qty", sa.Integer(), nullable=True),
        sa.Column("seller", sa.String(), nullable=True),
        sa.Column("region", sa.String(), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("seen_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("import_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["canonical_model"], ["models.model"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["import_id"], ["import_batches.import_id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for faster lookups and filtering
    op.create_index("idx_scored_listings_canonical_model", "scored_listings", ["canonical_model"], unique=False)
    op.create_index("idx_scored_listings_score", "scored_listings", ["score"], unique=False)
    op.create_index("idx_scored_listings_region", "scored_listings", ["region"], unique=False)
    op.create_index("idx_scored_listings_seen_at", "scored_listings", ["seen_at"], unique=False)
    op.create_index("idx_scored_listings_import_id", "scored_listings", ["import_id"], unique=False)

    # Quantized Listings table
    op.create_table(
        "quantized_listings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("scored_listing_id", sa.Integer(), nullable=False),
        sa.Column("model_7b", sa.Integer(), nullable=False),
        sa.Column("model_13b", sa.Integer(), nullable=False),
        sa.Column("model_70b", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("import_id", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["import_id"], ["import_batches.import_id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["scored_listing_id"], ["scored_listings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create index for faster lookups
    op.create_index(
        "idx_quantized_listings_scored_listing_id", "quantized_listings", ["scored_listing_id"], unique=False
    )

    # Create triggers to update the updated_at timestamp when records are modified
    op.execute(
        """
    CREATE TRIGGER IF NOT EXISTS update_models_timestamp
    AFTER UPDATE ON models
    BEGIN
        UPDATE models SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """
    )

    op.execute(
        """
    CREATE TRIGGER IF NOT EXISTS update_listings_timestamp
    AFTER UPDATE ON listings
    BEGIN
        UPDATE listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """
    )

    op.execute(
        """
    CREATE TRIGGER IF NOT EXISTS update_scored_listings_timestamp
    AFTER UPDATE ON scored_listings
    BEGIN
        UPDATE scored_listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """
    )

    op.execute(
        """
    CREATE TRIGGER IF NOT EXISTS update_quantized_listings_timestamp
    AFTER UPDATE ON quantized_listings
    BEGIN
        UPDATE quantized_listings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """
    )


def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS update_quantized_listings_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_scored_listings_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_listings_timestamp")
    op.execute("DROP TRIGGER IF EXISTS update_models_timestamp")

    # Drop tables
    op.drop_table("quantized_listings")
    op.drop_table("scored_listings")
    op.drop_table("listings")
    op.drop_table("models")
    op.drop_table("import_batches")
    op.drop_table("schema_version")
