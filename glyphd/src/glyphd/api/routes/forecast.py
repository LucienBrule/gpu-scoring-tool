"""
FastAPI route for forecasting and delta analysis endpoints.
"""

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from glyphd.core.dependencies.storage import get_storage_engine
from glyphd.core.storage.sqlite_store import SqliteListingStore
from glyphd.sqlite.models import ListingDelta

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"],
)


class ListingDeltaDTO:
    """
    Data Transfer Object for listing delta information.
    
    Represents a computed delta between two listing snapshots.
    """
    
    def __init__(self, delta: ListingDelta):
        self.id = delta.id
        self.model = delta.model
        self.price_delta = delta.price_delta
        self.price_delta_pct = delta.price_delta_pct
        self.score_delta = delta.score_delta
        self.region = delta.region
        self.source_url = delta.source_url
        self.timestamp = delta.timestamp
        self.current_snapshot_id = delta.current_snapshot_id
        self.previous_snapshot_id = delta.previous_snapshot_id
    
    def to_dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "price_delta": self.price_delta,
            "price_delta_pct": self.price_delta_pct,
            "score_delta": self.score_delta,
            "region": self.region,
            "source_url": self.source_url,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "current_snapshot_id": self.current_snapshot_id,
            "previous_snapshot_id": self.previous_snapshot_id,
        }


@router.get(
    "/deltas",
    summary="Get listing price deltas",
    description="Retrieve computed deltas between successive listing snapshots for price volatility analysis",
)
def get_listing_deltas(
    model: Optional[str] = Query(None, description="Filter by GPU model name"),
    min_price_change_pct: Optional[float] = Query(None, description="Minimum price change percentage"),
    after: Optional[datetime] = Query(None, description="Filter deltas after this timestamp"),
    region: Optional[str] = Query(None, description="Filter by region"),
    limit: int = Query(100, description="Maximum number of results to return", le=1000),
    storage: SqliteListingStore = Depends(get_storage_engine),
) -> List[dict]:
    """
    Get listing deltas with optional filtering.
    
    Args:
        model: Optional GPU model filter
        min_price_change_pct: Optional minimum price change percentage filter
        after: Optional timestamp filter
        region: Optional region filter
        limit: Maximum number of results
        storage: SQLite storage engine (injected dependency)
        
    Returns:
        List of delta records as dictionaries
    """
    try:
        # Get database session
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=storage.engine)
        session = Session()
        
        try:
            # Build query with filters
            query = session.query(ListingDelta)
            
            if model:
                query = query.filter(ListingDelta.model == model)
            
            if min_price_change_pct is not None:
                # Filter by absolute percentage change
                query = query.filter(
                    (ListingDelta.price_delta_pct >= min_price_change_pct) |
                    (ListingDelta.price_delta_pct <= -min_price_change_pct)
                )
            
            if after:
                query = query.filter(ListingDelta.timestamp >= after)
            
            if region:
                query = query.filter(ListingDelta.region == region)
            
            # Order by timestamp descending and limit results
            deltas = query.order_by(ListingDelta.timestamp.desc()).limit(limit).all()
            
            # Convert to DTOs and return as dictionaries
            result = [ListingDeltaDTO(delta).to_dict() for delta in deltas]
            
            logger.info(f"Retrieved {len(result)} deltas with filters: model={model}, min_change={min_price_change_pct}%, after={after}, region={region}")
            
            return result
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Failed to retrieve deltas: {e}")
        raise


@router.get(
    "/deltas/{delta_id}",
    summary="Get specific listing delta",
    description="Retrieve a specific delta by ID with full snapshot details",
)
def get_listing_delta(
    delta_id: int,
    storage: SqliteListingStore = Depends(get_storage_engine),
) -> dict:
    """
    Get a specific listing delta by ID.
    
    Args:
        delta_id: ID of the delta to retrieve
        storage: SQLite storage engine (injected dependency)
        
    Returns:
        Delta record with snapshot details
    """
    try:
        # Get database session
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=storage.engine)
        session = Session()
        
        try:
            # Query delta with snapshot relationships
            delta = session.query(ListingDelta).filter(
                ListingDelta.id == delta_id
            ).first()
            
            if not delta:
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail=f"Delta {delta_id} not found")
            
            # Convert to DTO and return
            result = ListingDeltaDTO(delta).to_dict()
            
            # Add snapshot details if available
            if delta.current_snapshot:
                result["current_snapshot"] = {
                    "id": delta.current_snapshot.id,
                    "price_usd": delta.current_snapshot.price_usd,
                    "score": delta.current_snapshot.score,
                    "seen_at": delta.current_snapshot.seen_at.isoformat() if delta.current_snapshot.seen_at else None,
                }
            
            if delta.previous_snapshot:
                result["previous_snapshot"] = {
                    "id": delta.previous_snapshot.id,
                    "price_usd": delta.previous_snapshot.price_usd,
                    "score": delta.previous_snapshot.score,
                    "seen_at": delta.previous_snapshot.seen_at.isoformat() if delta.previous_snapshot.seen_at else None,
                }
            
            logger.info(f"Retrieved delta {delta_id}")
            return result
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Failed to retrieve delta {delta_id}: {e}")
        raise