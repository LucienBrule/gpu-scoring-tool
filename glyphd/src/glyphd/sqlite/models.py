"""
SQLAlchemy models for the GPU Scoring Tool SQLite database.

This module defines the SQLAlchemy ORM models that correspond to the tables in the SQLite schema.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SchemaVersion(Base):
    """Model for tracking schema versions and migrations."""

    __tablename__ = "schema_version"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String, nullable=False)
    applied_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(Text)


class ImportBatch(Base):
    """Model for tracking import batches and enabling differential updates."""

    __tablename__ = "import_batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(String, nullable=False, unique=True)
    imported_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    source = Column(String)
    record_count = Column(Integer, default=0)
    description = Column(Text)

    # Relationships
    models = relationship("Model", back_populates="import_batch")
    listings = relationship("Listing", back_populates="import_batch")
    scored_listings = relationship("ScoredListing", back_populates="import_batch")
    quantized_listings = relationship("QuantizedListing", back_populates="import_batch")


class Model(Base):
    """
    Model for GPU models with technical specifications.

    Based on GPUModelDTO, stores normalized GPU model registry with technical specifications.
    """

    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model = Column(String, nullable=False, unique=True)

    # Technical specifications
    vram_gb = Column(Integer)
    tdp_watts = Column(Integer)
    mig_support = Column(Integer, default=0)
    nvlink = Column(Boolean, default=False)
    generation = Column(String)
    cuda_cores = Column(Integer)
    slot_width = Column(Integer)
    pcie_generation = Column(Integer)

    # Market data (aggregated from listings)
    listing_count = Column(Integer, default=0)
    min_price = Column(Float)
    median_price = Column(Float)
    max_price = Column(Float)
    avg_price = Column(Float)

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    import_id = Column(String, ForeignKey("import_batches.import_id", ondelete="SET NULL"))

    # Relationships
    import_batch = relationship("ImportBatch", back_populates="models")
    listings = relationship("Listing", back_populates="model")
    scored_listings = relationship("ScoredListing", back_populates="model")


class Listing(Base):
    """
    Model for raw GPU listings.

    Based on GPUListingDTO from glyphsieve, stores raw listing metadata parsed from CSV input.
    """

    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    canonical_model = Column(String, ForeignKey("models.model", ondelete="CASCADE"), nullable=False)
    match_type = Column(String, nullable=False)
    match_score = Column(Float, nullable=False)

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    import_id = Column(String, ForeignKey("import_batches.import_id", ondelete="SET NULL"))

    # Relationships
    model = relationship("Model", back_populates="listings")
    import_batch = relationship("ImportBatch", back_populates="listings")


class ScoredListing(Base):
    """
    Model for enriched and scored GPU listings.

    Based on GPUListingDTO from glyphd and EnrichedGPUListingDTO, stores enriched and scored GPU listings.
    """

    __tablename__ = "scored_listings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Basic listing information
    canonical_model = Column(String, ForeignKey("models.model", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)

    # Enriched fields from GPU metadata
    vram_gb = Column(Integer, nullable=False)
    tdp_watts = Column(Integer, nullable=False)
    mig_support = Column(Integer, default=0)
    nvlink = Column(Boolean, default=False)

    # Optional enriched fields
    generation = Column(String)
    cuda_cores = Column(Integer)
    slot_width = Column(Integer)
    pcie_generation = Column(Integer)

    # Additional fields from EnrichedGPUListingDTO
    form_factor = Column(String, default="Standard")
    notes = Column(Text)
    warnings = Column(Text)

    # Scoring information
    score = Column(Float, nullable=False)

    # Additional fields from EPIC.persist.sqlite-store requirements
    condition = Column(String)
    quantity = Column(Integer)
    min_order_qty = Column(Integer)
    seller = Column(String)
    region = Column(String)
    source_url = Column(Text)
    source_type = Column(String)
    seen_at = Column(DateTime)

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    import_id = Column(String, ForeignKey("import_batches.import_id", ondelete="SET NULL"))

    # Relationships
    model = relationship("Model", back_populates="scored_listings")
    import_batch = relationship("ImportBatch", back_populates="scored_listings")
    quantized_listing = relationship("QuantizedListing", back_populates="scored_listing", uselist=False)


class QuantizedListing(Base):
    """
    Model for quantization capacities for GPU listings.

    Based on QuantizationCapacitySpec, stores quantization capacities for GPU listings.
    """

    __tablename__ = "quantized_listings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scored_listing_id = Column(Integer, ForeignKey("scored_listings.id", ondelete="CASCADE"), nullable=False)
    model_7b = Column(Integer, nullable=False)
    model_13b = Column(Integer, nullable=False)
    model_70b = Column(Integer, nullable=False)

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    import_id = Column(String, ForeignKey("import_batches.import_id", ondelete="SET NULL"))

    # Relationships
    scored_listing = relationship("ScoredListing", back_populates="quantized_listing")
    import_batch = relationship("ImportBatch", back_populates="quantized_listings")
