"""
Core forecasting functionality for GPU listing price history and delta tracking.

This module provides functionality to capture listing snapshots and compute
deltas between successive snapshots for price volatility analysis and forecasting.
"""

from datetime import datetime
from typing import Optional

from glyphd.sqlite.models import ListingDelta, ListingSnapshot


def compute_delta(prev: ListingSnapshot, curr: ListingSnapshot) -> ListingDelta:
    """
    Compute delta between two listing snapshots.
    
    Args:
        prev: Previous snapshot
        curr: Current snapshot
        
    Returns:
        ListingDelta: Computed delta with price and score changes
        
    Raises:
        ValueError: If snapshots are for different models or sources
        ZeroDivisionError: If previous price is zero (handled gracefully)
    """
    # Validate that snapshots are comparable
    if prev.model != curr.model:
        raise ValueError(f"Cannot compute delta between different models: {prev.model} vs {curr.model}")
    
    if prev.source_url != curr.source_url:
        raise ValueError(f"Cannot compute delta between different sources: {prev.source_url} vs {curr.source_url}")
    
    # Compute price delta
    price_delta = curr.price_usd - prev.price_usd
    
    # Compute percentage change, handling zero division
    if prev.price_usd == 0:
        price_delta_pct = 0.0  # No meaningful percentage change from zero
    else:
        price_delta_pct = (price_delta / prev.price_usd) * 100
    
    # Compute score delta
    score_delta = curr.score - prev.score
    
    # Create and return delta object
    return ListingDelta(
        current_snapshot_id=curr.id,
        previous_snapshot_id=prev.id,
        price_delta=price_delta,
        price_delta_pct=price_delta_pct,
        score_delta=score_delta,
        model=curr.model,
        region=curr.region,
        source_url=curr.source_url,
        timestamp=datetime.utcnow(),
    )


def create_snapshot_from_listing(listing_data: dict, seen_at: Optional[datetime] = None) -> ListingSnapshot:
    """
    Create a ListingSnapshot from listing data.
    
    Args:
        listing_data: Dictionary containing listing information
        seen_at: Timestamp when listing was seen (defaults to now)
        
    Returns:
        ListingSnapshot: New snapshot object
    """
    if seen_at is None:
        seen_at = datetime.utcnow()
    
    return ListingSnapshot(
        model=listing_data.get('canonical_model', listing_data.get('model')),
        price_usd=float(listing_data['price']),
        score=float(listing_data['score']),
        quantization_capacity=listing_data.get('quantization_capacity'),
        seen_at=seen_at,
        seller=listing_data.get('seller'),
        region=listing_data.get('region'),
        source_url=listing_data.get('source_url'),
        heuristics=listing_data.get('heuristics'),
    )


__all__ = [
    "ListingDelta",
    "ListingSnapshot",
    "compute_delta",
    "create_snapshot_from_listing",
]