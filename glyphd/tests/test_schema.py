"""
Test the SQLite schema for the GPU Scoring Tool.

This script verifies that the schema can be instantiated and used correctly.
"""

import os
import tempfile
import unittest
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Session

from glyphd.sqlite.models import (
    Base,
    ImportBatch,
    Listing,
    Model,
    QuantizedListing,
    SchemaVersion,
    ScoredListing,
)


class TestSchema(unittest.TestCase):
    """Test the SQLite schema for the GPU Scoring Tool."""

    def setUp(self):
        """Set up a temporary database for testing."""
        # Create a temporary file for the database
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db_file.close()

        # Create an engine connected to the temporary database
        self.engine = sa.create_engine(f"sqlite:///{self.temp_db_file.name}")

        # Create all tables
        Base.metadata.create_all(self.engine)

        # Create a session
        self.session = Session(self.engine)

        # Insert initial schema version
        schema_version = SchemaVersion(
            version="1.0.0",
            description="Initial schema creation",
        )
        self.session.add(schema_version)
        self.session.commit()

    def tearDown(self):
        """Clean up after the test."""
        # Close the session
        self.session.close()

        # Remove the temporary database file
        os.unlink(self.temp_db_file.name)

    def test_schema_version(self):
        """Test that the schema version table works correctly."""
        # Query the schema version
        schema_version = self.session.query(SchemaVersion).first()

        # Check that the schema version is correct
        self.assertEqual(schema_version.version, "1.0.0")
        self.assertEqual(schema_version.description, "Initial schema creation")

    def test_import_batch(self):
        """Test that the import batch table works correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-1",
            source="test",
            record_count=10,
            description="Test import batch",
        )
        self.session.add(import_batch)
        self.session.commit()

        # Query the import batch
        queried_batch = self.session.query(ImportBatch).filter_by(import_id="test-import-1").first()

        # Check that the import batch is correct
        self.assertEqual(queried_batch.import_id, "test-import-1")
        self.assertEqual(queried_batch.source, "test")
        self.assertEqual(queried_batch.record_count, 10)
        self.assertEqual(queried_batch.description, "Test import batch")

    def test_model(self):
        """Test that the model table works correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-2",
            source="test",
            description="Test import batch for models",
        )
        self.session.add(import_batch)
        self.session.commit()

        # Create a model
        model = Model(
            model="H100_PCIE_80GB",
            vram_gb=80,
            tdp_watts=350,
            mig_support=7,
            nvlink=True,
            generation="Hopper",
            cuda_cores=18176,
            slot_width=2,
            pcie_generation=5,
            listing_count=7,
            min_price=23800.0,
            median_price=34995.0,
            max_price=49999.0,
            avg_price=34024.71,
            import_id="test-import-2",
        )
        self.session.add(model)
        self.session.commit()

        # Query the model
        queried_model = self.session.query(Model).filter_by(model="H100_PCIE_80GB").first()

        # Check that the model is correct
        self.assertEqual(queried_model.model, "H100_PCIE_80GB")
        self.assertEqual(queried_model.vram_gb, 80)
        self.assertEqual(queried_model.tdp_watts, 350)
        self.assertEqual(queried_model.mig_support, 7)
        self.assertTrue(queried_model.nvlink)
        self.assertEqual(queried_model.generation, "Hopper")
        self.assertEqual(queried_model.cuda_cores, 18176)
        self.assertEqual(queried_model.slot_width, 2)
        self.assertEqual(queried_model.pcie_generation, 5)
        self.assertEqual(queried_model.listing_count, 7)
        self.assertEqual(queried_model.min_price, 23800.0)
        self.assertEqual(queried_model.median_price, 34995.0)
        self.assertEqual(queried_model.max_price, 49999.0)
        self.assertEqual(queried_model.avg_price, 34024.71)
        self.assertEqual(queried_model.import_id, "test-import-2")

    def test_listing(self):
        """Test that the listing table works correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-3",
            source="test",
            description="Test import batch for listings",
        )
        self.session.add(import_batch)

        # Create a model
        model = Model(
            model="RTX_A5000",
            vram_gb=24,
            tdp_watts=230,
            generation="Ampere",
        )
        self.session.add(model)
        self.session.commit()

        # Create a listing
        listing = Listing(
            title="NVIDIA RTX A5000 24GB Graphics Card",
            price=2500.0,
            canonical_model="RTX_A5000",
            match_type="exact",
            match_score=1.0,
            import_id="test-import-3",
        )
        self.session.add(listing)
        self.session.commit()

        # Query the listing
        queried_listing = self.session.query(Listing).first()

        # Check that the listing is correct
        self.assertEqual(queried_listing.title, "NVIDIA RTX A5000 24GB Graphics Card")
        self.assertEqual(queried_listing.price, 2500.0)
        self.assertEqual(queried_listing.canonical_model, "RTX_A5000")
        self.assertEqual(queried_listing.match_type, "exact")
        self.assertEqual(queried_listing.match_score, 1.0)
        self.assertEqual(queried_listing.import_id, "test-import-3")

        # Check the relationship with the model
        self.assertEqual(queried_listing.model.model, "RTX_A5000")
        self.assertEqual(queried_listing.model.vram_gb, 24)

    def test_scored_listing(self):
        """Test that the scored listing table works correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-4",
            source="test",
            description="Test import batch for scored listings",
        )
        self.session.add(import_batch)

        # Create a model
        model = Model(
            model="RTX_A6000",
            vram_gb=48,
            tdp_watts=300,
            generation="Ampere",
        )
        self.session.add(model)
        self.session.commit()

        # Create a scored listing
        scored_listing = ScoredListing(
            canonical_model="RTX_A6000",
            price=4500.0,
            vram_gb=48,
            tdp_watts=300,
            mig_support=0,
            nvlink=True,
            generation="Ampere",
            form_factor="Standard",
            score=0.85,
            condition="new",
            quantity=1,
            min_order_qty=1,
            seller="GPU Store",
            region="US",
            source_url="https://example.com/rtx-a6000",
            source_type="marketplace",
            seen_at=datetime.utcnow(),
            import_id="test-import-4",
        )
        self.session.add(scored_listing)
        self.session.commit()

        # Query the scored listing
        queried_scored_listing = self.session.query(ScoredListing).first()

        # Check that the scored listing is correct
        self.assertEqual(queried_scored_listing.canonical_model, "RTX_A6000")
        self.assertEqual(queried_scored_listing.price, 4500.0)
        self.assertEqual(queried_scored_listing.vram_gb, 48)
        self.assertEqual(queried_scored_listing.tdp_watts, 300)
        self.assertEqual(queried_scored_listing.mig_support, 0)
        self.assertTrue(queried_scored_listing.nvlink)
        self.assertEqual(queried_scored_listing.generation, "Ampere")
        self.assertEqual(queried_scored_listing.form_factor, "Standard")
        self.assertEqual(queried_scored_listing.score, 0.85)
        self.assertEqual(queried_scored_listing.condition, "new")
        self.assertEqual(queried_scored_listing.quantity, 1)
        self.assertEqual(queried_scored_listing.min_order_qty, 1)
        self.assertEqual(queried_scored_listing.seller, "GPU Store")
        self.assertEqual(queried_scored_listing.region, "US")
        self.assertEqual(queried_scored_listing.source_url, "https://example.com/rtx-a6000")
        self.assertEqual(queried_scored_listing.source_type, "marketplace")
        self.assertIsNotNone(queried_scored_listing.seen_at)
        self.assertEqual(queried_scored_listing.import_id, "test-import-4")

        # Check the relationship with the model
        self.assertEqual(queried_scored_listing.model.model, "RTX_A6000")
        self.assertEqual(queried_scored_listing.model.vram_gb, 48)

    def test_quantized_listing(self):
        """Test that the quantized listing table works correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-5",
            source="test",
            description="Test import batch for quantized listings",
        )
        self.session.add(import_batch)

        # Create a model
        model = Model(
            model="H100_SXM5_80GB",
            vram_gb=80,
            tdp_watts=700,
            generation="Hopper",
        )
        self.session.add(model)

        # Create a scored listing
        scored_listing = ScoredListing(
            canonical_model="H100_SXM5_80GB",
            price=30000.0,
            vram_gb=80,
            tdp_watts=700,
            mig_support=7,
            nvlink=True,
            generation="Hopper",
            score=0.95,
            import_id="test-import-5",
        )
        self.session.add(scored_listing)
        self.session.commit()

        # Create a quantized listing
        quantized_listing = QuantizedListing(
            scored_listing_id=scored_listing.id,
            model_7b=10,
            model_13b=5,
            model_70b=1,
            import_id="test-import-5",
        )
        self.session.add(quantized_listing)
        self.session.commit()

        # Query the quantized listing
        queried_quantized_listing = self.session.query(QuantizedListing).first()

        # Check that the quantized listing is correct
        self.assertEqual(queried_quantized_listing.scored_listing_id, scored_listing.id)
        self.assertEqual(queried_quantized_listing.model_7b, 10)
        self.assertEqual(queried_quantized_listing.model_13b, 5)
        self.assertEqual(queried_quantized_listing.model_70b, 1)
        self.assertEqual(queried_quantized_listing.import_id, "test-import-5")

        # Check the relationship with the scored listing
        self.assertEqual(queried_quantized_listing.scored_listing.canonical_model, "H100_SXM5_80GB")
        self.assertEqual(queried_quantized_listing.scored_listing.vram_gb, 80)

        # Check the relationship with the model through the scored listing
        self.assertEqual(queried_quantized_listing.scored_listing.model.model, "H100_SXM5_80GB")
        self.assertEqual(queried_quantized_listing.scored_listing.model.generation, "Hopper")

    def test_relationships(self):
        """Test that the relationships between tables work correctly."""
        # Create an import batch
        import_batch = ImportBatch(
            import_id="test-import-6",
            source="test",
            description="Test import batch for relationships",
        )
        self.session.add(import_batch)

        # Create a model
        model = Model(
            model="RTX_4090",
            vram_gb=24,
            tdp_watts=450,
            generation="Ada",
            import_id="test-import-6",
        )
        self.session.add(model)
        self.session.commit()

        # Create a listing
        listing = Listing(
            title="NVIDIA GeForce RTX 4090 24GB",
            price=1599.0,
            canonical_model="RTX_4090",
            match_type="exact",
            match_score=1.0,
            import_id="test-import-6",
        )
        self.session.add(listing)

        # Create a scored listing
        scored_listing = ScoredListing(
            canonical_model="RTX_4090",
            price=1599.0,
            vram_gb=24,
            tdp_watts=450,
            generation="Ada",
            score=0.9,
            import_id="test-import-6",
        )
        self.session.add(scored_listing)
        self.session.commit()

        # Create a quantized listing
        quantized_listing = QuantizedListing(
            scored_listing_id=scored_listing.id,
            model_7b=3,
            model_13b=1,
            model_70b=0,
            import_id="test-import-6",
        )
        self.session.add(quantized_listing)
        self.session.commit()

        # Query the import batch and check its relationships
        queried_import_batch = self.session.query(ImportBatch).filter_by(import_id="test-import-6").first()
        self.assertEqual(len(queried_import_batch.models), 1)
        self.assertEqual(len(queried_import_batch.listings), 1)
        self.assertEqual(len(queried_import_batch.scored_listings), 1)
        self.assertEqual(len(queried_import_batch.quantized_listings), 1)

        # Query the model and check its relationships
        queried_model = self.session.query(Model).filter_by(model="RTX_4090").first()
        self.assertEqual(len(queried_model.listings), 1)
        self.assertEqual(len(queried_model.scored_listings), 1)

        # Query the scored listing and check its relationships
        queried_scored_listing = self.session.query(ScoredListing).filter_by(canonical_model="RTX_4090").first()
        self.assertIsNotNone(queried_scored_listing.quantized_listing)
        self.assertEqual(queried_scored_listing.quantized_listing.model_7b, 3)

    def test_sql_loader(self):
        """Test that schema.sql can be loaded via ResourceContext."""
        from glyphd.core.resources.resource_context import GlyphdResourceContext

        # Create a resource context
        resource_context = GlyphdResourceContext()

        # Load the schema.sql file
        schema_sql = resource_context.load_text("sql/schema.sql")

        # Verify that the schema SQL was loaded and contains expected content
        self.assertIsInstance(schema_sql, str)
        self.assertGreater(len(schema_sql), 0)

        # Check for some expected SQL keywords/statements in the schema
        self.assertIn("CREATE TABLE", schema_sql)
        self.assertIn("schema_version", schema_sql)
        self.assertIn("import_batches", schema_sql)
        self.assertIn("models", schema_sql)
        self.assertIn("scored_listings", schema_sql)


if __name__ == "__main__":
    unittest.main()
