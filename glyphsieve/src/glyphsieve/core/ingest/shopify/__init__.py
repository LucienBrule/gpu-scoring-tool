"""
Shopify-specific source loaders for the GPU Scoring Tool.

This module contains loaders for various Shopify-based vendors and their
specific data formats.
"""

from .wamatek_loader import WamatekShopifyLoader

__all__ = ["WamatekShopifyLoader"]
