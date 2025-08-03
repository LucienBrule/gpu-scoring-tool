"""
Unit tests for forecasting functionality.
"""

from datetime import datetime, timedelta

import pytest

from glyphd.core.forecast import compute_delta, create_snapshot_from_listing
from glyphd.sqlite.models import ListingSnapshot


class TestComputeDelta:
    """Test the compute_delta function."""
    
    def test_compute_delta_basic(self):
        """Test basic delta computation."""
        # Create mock snapshots
        prev_snapshot = ListingSnapshot(
            id=1,
            model="RTX_4090",
            price_usd=1500.0,
            score=85.0,
            seen_at=datetime.utcnow() - timedelta(hours=1),
            source_url="https://example.com/listing1",
            region="US",
        )
        
        curr_snapshot = ListingSnapshot(
            id=2,
            model="RTX_4090",
            price_usd=1600.0,
            score=87.0,
            seen_at=datetime.utcnow(),
            source_url="https://example.com/listing1",
            region="US",
        )
        
        # Compute delta
        delta = compute_delta(prev_snapshot, curr_snapshot)
        
        # Verify calculations
        assert delta.price_delta == 100.0
        assert abs(delta.price_delta_pct - 6.67) < 0.01  # 100/1500 * 100 ≈ 6.67%
        assert delta.score_delta == 2.0
        assert delta.model == "RTX_4090"
        assert delta.region == "US"
        assert delta.source_url == "https://example.com/listing1"
        assert delta.current_snapshot_id == 2
        assert delta.previous_snapshot_id == 1
    
    def test_compute_delta_price_decrease(self):
        """Test delta computation with price decrease."""
        prev_snapshot = ListingSnapshot(
            id=1,
            model="RTX_3080",
            price_usd=800.0,
            score=75.0,
            seen_at=datetime.utcnow() - timedelta(hours=1),
            source_url="https://example.com/listing2",
        )
        
        curr_snapshot = ListingSnapshot(
            id=2,
            model="RTX_3080",
            price_usd=700.0,
            score=73.0,
            seen_at=datetime.utcnow(),
            source_url="https://example.com/listing2",
        )
        
        delta = compute_delta(prev_snapshot, curr_snapshot)
        
        assert delta.price_delta == -100.0
        assert delta.price_delta_pct == -12.5  # -100/800 * 100 = -12.5%
        assert delta.score_delta == -2.0
    
    def test_compute_delta_zero_price(self):
        """Test delta computation with zero previous price."""
        prev_snapshot = ListingSnapshot(
            id=1,
            model="RTX_4090",
            price_usd=0.0,
            score=85.0,
            seen_at=datetime.utcnow() - timedelta(hours=1),
            source_url="https://example.com/listing3",
        )
        
        curr_snapshot = ListingSnapshot(
            id=2,
            model="RTX_4090",
            price_usd=1500.0,
            score=87.0,
            seen_at=datetime.utcnow(),
            source_url="https://example.com/listing3",
        )
        
        delta = compute_delta(prev_snapshot, curr_snapshot)
        
        assert delta.price_delta == 1500.0
        assert delta.price_delta_pct == 0.0  # No meaningful percentage from zero
        assert delta.score_delta == 2.0
    
    def test_compute_delta_different_models_error(self):
        """Test that computing delta between different models raises error."""
        prev_snapshot = ListingSnapshot(
            id=1,
            model="RTX_4090",
            price_usd=1500.0,
            score=85.0,
            seen_at=datetime.utcnow() - timedelta(hours=1),
            source_url="https://example.com/listing1",
        )
        
        curr_snapshot = ListingSnapshot(
            id=2,
            model="RTX_3080",  # Different model
            price_usd=800.0,
            score=75.0,
            seen_at=datetime.utcnow(),
            source_url="https://example.com/listing1",
        )
        
        with pytest.raises(ValueError, match="Cannot compute delta between different models"):
            compute_delta(prev_snapshot, curr_snapshot)
    
    def test_compute_delta_different_sources_error(self):
        """Test that computing delta between different sources raises error."""
        prev_snapshot = ListingSnapshot(
            id=1,
            model="RTX_4090",
            price_usd=1500.0,
            score=85.0,
            seen_at=datetime.utcnow() - timedelta(hours=1),
            source_url="https://example.com/listing1",
        )
        
        curr_snapshot = ListingSnapshot(
            id=2,
            model="RTX_4090",
            price_usd=1600.0,
            score=87.0,
            seen_at=datetime.utcnow(),
            source_url="https://example.com/listing2",  # Different source
        )
        
        with pytest.raises(ValueError, match="Cannot compute delta between different sources"):
            compute_delta(prev_snapshot, curr_snapshot)


class TestCreateSnapshotFromListing:
    """Test the create_snapshot_from_listing function."""
    
    def test_create_snapshot_basic(self):
        """Test basic snapshot creation."""
        listing_data = {
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 85.0,
            'seller': 'TechStore',
            'region': 'US',
            'source_url': 'https://example.com/listing1',
            'quantization_capacity': {'7b': 4, '13b': 2, '70b': 0},
            'heuristics': {'confidence': 0.95},
        }
        
        snapshot = create_snapshot_from_listing(listing_data)
        
        assert snapshot.model == 'RTX_4090'
        assert snapshot.price_usd == 1500.0
        assert snapshot.score == 85.0
        assert snapshot.seller == 'TechStore'
        assert snapshot.region == 'US'
        assert snapshot.source_url == 'https://example.com/listing1'
        assert snapshot.quantization_capacity == {'7b': 4, '13b': 2, '70b': 0}
        assert snapshot.heuristics == {'confidence': 0.95}
        assert isinstance(snapshot.seen_at, datetime)
    
    def test_create_snapshot_with_model_field(self):
        """Test snapshot creation with 'model' field instead of 'canonical_model'."""
        listing_data = {
            'model': 'RTX_3080',  # Using 'model' instead of 'canonical_model'
            'price': 800.0,
            'score': 75.0,
        }
        
        snapshot = create_snapshot_from_listing(listing_data)
        
        assert snapshot.model == 'RTX_3080'
        assert snapshot.price_usd == 800.0
        assert snapshot.score == 75.0
    
    def test_create_snapshot_minimal_data(self):
        """Test snapshot creation with minimal required data."""
        listing_data = {
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 85.0,
        }
        
        snapshot = create_snapshot_from_listing(listing_data)
        
        assert snapshot.model == 'RTX_4090'
        assert snapshot.price_usd == 1500.0
        assert snapshot.score == 85.0
        assert snapshot.seller is None
        assert snapshot.region is None
        assert snapshot.source_url is None
        assert snapshot.quantization_capacity is None
        assert snapshot.heuristics is None
    
    def test_create_snapshot_custom_seen_at(self):
        """Test snapshot creation with custom seen_at timestamp."""
        custom_time = datetime(2025, 1, 1, 12, 0, 0)
        listing_data = {
            'canonical_model': 'RTX_4090',
            'price': 1500.0,
            'score': 85.0,
        }
        
        snapshot = create_snapshot_from_listing(listing_data, seen_at=custom_time)
        
        assert snapshot.seen_at == custom_time


class TestSnapshotValidation:
    """Test snapshot validation scenarios."""
    
    def test_no_delta_for_single_snapshot(self):
        """Test that no delta is created when only one snapshot exists."""
        # This test would be part of integration testing
        # since it requires database interaction
        pass
    
    def test_delta_creation_workflow(self):
        """Test the complete workflow of snapshot and delta creation."""
        # This test would be part of integration testing
        # since it requires database interaction and the full ingestion pipeline
        pass