"""
Unit tests for ML train/test split functionality.

Tests the stratified splitting, balance validation, and split summary functions.
"""

import pandas as pd
import pytest

from glyphsieve.ml.train_test_split import (
    get_split_summary,
    stratified_split,
    validate_split_balance,
)


class TestStratifiedSplit:
    """Test the stratified train/test split functionality."""

    def create_balanced_dataset(self, total_samples=1000, gpu_ratio=0.4):
        """Helper to create a balanced test dataset."""
        gpu_count = int(total_samples * gpu_ratio)
        non_gpu_count = total_samples - gpu_count

        data = {
            "title": [f"GPU_{i}" for i in range(gpu_count)] + [f"NonGPU_{i}" for i in range(non_gpu_count)],
            "bulk_notes": [f"Description_{i}" for i in range(total_samples)],
            "is_gpu": [1] * gpu_count + [0] * non_gpu_count,
        }

        return pd.DataFrame(data)

    def test_stratified_split_basic(self):
        """Test basic stratified split functionality."""
        df = self.create_balanced_dataset(100, 0.4)

        train_df, test_df, metadata = stratified_split(df, test_size=0.2, random_seed=42)

        # Check split sizes
        assert len(train_df) == 80
        assert len(test_df) == 20
        assert len(train_df) + len(test_df) == len(df)

        # Check columns are preserved
        assert list(train_df.columns) == ["title", "bulk_notes", "is_gpu"]
        assert list(test_df.columns) == ["title", "bulk_notes", "is_gpu"]

        # Check class balance is preserved
        original_gpu_ratio = df["is_gpu"].mean()
        train_gpu_ratio = train_df["is_gpu"].mean()
        test_gpu_ratio = test_df["is_gpu"].mean()

        # Should be close to original ratio (within 5% for small dataset)
        assert abs(train_gpu_ratio - original_gpu_ratio) < 0.05
        assert abs(test_gpu_ratio - original_gpu_ratio) < 0.05

        # Check metadata
        assert metadata["total_samples"] == 100
        assert metadata["train_size"] == 80
        assert metadata["test_size"] == 20
        assert metadata["train_test_ratio"] == "80/20"
        assert metadata["random_seed"] == 42
        assert "balance_preserved" in metadata
        assert "max_balance_difference" in metadata

    def test_stratified_split_different_test_sizes(self):
        """Test stratified split with different test sizes."""
        df = self.create_balanced_dataset(1000, 0.3)

        # Test 70/30 split
        train_df, test_df, metadata = stratified_split(df, test_size=0.3)
        assert len(train_df) == 700
        assert len(test_df) == 300
        assert metadata["train_test_ratio"] == "70/30"

        # Test 90/10 split
        train_df, test_df, metadata = stratified_split(df, test_size=0.1)
        assert len(train_df) == 900
        assert len(test_df) == 100
        assert metadata["train_test_ratio"] == "90/10"

    def test_stratified_split_reproducibility(self):
        """Test that splits are reproducible with same random seed."""
        df = self.create_balanced_dataset(200, 0.5)

        # Split with same seed twice
        train_df1, test_df1, _ = stratified_split(df, random_seed=123)
        train_df2, test_df2, _ = stratified_split(df, random_seed=123)

        # Should be identical
        pd.testing.assert_frame_equal(train_df1.sort_index(), train_df2.sort_index())
        pd.testing.assert_frame_equal(test_df1.sort_index(), test_df2.sort_index())

        # Split with different seed
        train_df3, test_df3, _ = stratified_split(df, random_seed=456)

        # Should be different
        assert not train_df1.equals(train_df3)
        assert not test_df1.equals(test_df3)

    def test_stratified_split_edge_cases(self):
        """Test stratified split with edge cases."""
        # Very small dataset
        small_df = pd.DataFrame(
            {
                "title": ["GPU1", "GPU2", "NonGPU1", "NonGPU2"],
                "bulk_notes": ["Desc1", "Desc2", "Desc3", "Desc4"],
                "is_gpu": [1, 1, 0, 0],
            }
        )

        train_df, test_df, metadata = stratified_split(small_df, test_size=0.5)
        assert len(train_df) == 2
        assert len(test_df) == 2

        # Check that both classes are represented in both splits
        assert train_df["is_gpu"].sum() >= 1  # At least one GPU
        assert (train_df["is_gpu"] == 0).sum() >= 1  # At least one non-GPU
        assert test_df["is_gpu"].sum() >= 1  # At least one GPU
        assert (test_df["is_gpu"] == 0).sum() >= 1  # At least one non-GPU

    def test_stratified_split_imbalanced_data(self):
        """Test stratified split with highly imbalanced data."""
        # 90% GPU, 10% non-GPU
        df = self.create_balanced_dataset(1000, 0.9)

        train_df, test_df, metadata = stratified_split(df, test_size=0.2)

        # Check that class ratios are preserved
        original_gpu_ratio = df["is_gpu"].mean()
        train_gpu_ratio = train_df["is_gpu"].mean()
        test_gpu_ratio = test_df["is_gpu"].mean()

        # Should be close to 0.9
        assert abs(train_gpu_ratio - original_gpu_ratio) < 0.02
        assert abs(test_gpu_ratio - original_gpu_ratio) < 0.02

        # Check metadata reflects imbalance
        assert metadata["total_samples"] == 1000

    def test_stratified_split_missing_is_gpu_column(self):
        """Test error handling when is_gpu column is missing."""
        df = pd.DataFrame(
            {
                "title": ["GPU1", "GPU2"],
                "bulk_notes": ["Desc1", "Desc2"],
                # Missing is_gpu column
            }
        )

        with pytest.raises(ValueError, match="DataFrame must contain 'is_gpu' column"):
            stratified_split(df)

    def test_stratified_split_empty_dataset(self):
        """Test error handling with empty dataset."""
        empty_df = pd.DataFrame({"title": [], "bulk_notes": [], "is_gpu": []})

        with pytest.raises(ValueError, match="Cannot split empty dataset"):
            stratified_split(empty_df)


class TestSplitBalanceValidation:
    """Test the split balance validation functionality."""

    def test_validate_split_balance_good(self):
        """Test validation with well-balanced splits."""
        train_df = pd.DataFrame(
            {
                "title": ["GPU1", "GPU2", "NonGPU1", "NonGPU2"],
                "bulk_notes": ["Desc1", "Desc2", "Desc3", "Desc4"],
                "is_gpu": [1, 1, 0, 0],  # 50% GPU
            }
        )

        test_df = pd.DataFrame(
            {"title": ["GPU3", "NonGPU3"], "bulk_notes": ["Desc5", "Desc6"], "is_gpu": [1, 0]}  # 50% GPU
        )

        # Should pass validation (0% difference)
        assert validate_split_balance(train_df, test_df, tolerance=0.02)

    def test_validate_split_balance_within_tolerance(self):
        """Test validation with balance within tolerance."""
        train_df = pd.DataFrame(
            {
                "title": ["GPU1", "GPU2", "NonGPU1", "NonGPU2"],
                "bulk_notes": ["Desc1", "Desc2", "Desc3", "Desc4"],
                "is_gpu": [1, 1, 0, 0],  # 50% GPU
            }
        )

        test_df = pd.DataFrame(
            {
                "title": ["GPU3", "GPU4", "NonGPU3"],
                "bulk_notes": ["Desc5", "Desc6", "Desc7"],
                "is_gpu": [1, 1, 0],  # 66.7% GPU (16.7% difference)
            }
        )

        # Should fail with 2% tolerance but pass with 20% tolerance
        assert not validate_split_balance(train_df, test_df, tolerance=0.02)
        assert validate_split_balance(train_df, test_df, tolerance=0.20)

    def test_validate_split_balance_outside_tolerance(self):
        """Test validation with balance outside tolerance."""
        train_df = pd.DataFrame(
            {
                "title": ["GPU1", "NonGPU1", "NonGPU2", "NonGPU3"],
                "bulk_notes": ["Desc1", "Desc2", "Desc3", "Desc4"],
                "is_gpu": [1, 0, 0, 0],  # 25% GPU
            }
        )

        test_df = pd.DataFrame(
            {
                "title": ["GPU2", "GPU3", "GPU4", "NonGPU4"],
                "bulk_notes": ["Desc5", "Desc6", "Desc7", "Desc8"],
                "is_gpu": [1, 1, 1, 0],  # 75% GPU (50% difference)
            }
        )

        # Should fail validation
        assert not validate_split_balance(train_df, test_df, tolerance=0.02)
        assert not validate_split_balance(train_df, test_df, tolerance=0.10)


class TestSplitSummary:
    """Test the split summary functionality."""

    def test_get_split_summary(self):
        """Test split summary generation."""
        train_df = pd.DataFrame(
            {
                "title": ["GPU1", "GPU2", "GPU3", "NonGPU1", "NonGPU2"],
                "bulk_notes": ["Desc1", "Desc2", "Desc3", "Desc4", "Desc5"],
                "is_gpu": [1, 1, 1, 0, 0],  # 3 GPU, 2 non-GPU
            }
        )

        test_df = pd.DataFrame(
            {"title": ["GPU4", "NonGPU3"], "bulk_notes": ["Desc6", "Desc7"], "is_gpu": [1, 0]}  # 1 GPU, 1 non-GPU
        )

        summary = get_split_summary(train_df, test_df)

        # Check summary contents
        assert summary["total_samples"] == 7
        assert summary["train_samples"] == 5
        assert summary["test_samples"] == 2
        assert summary["train_gpu_count"] == 3
        assert summary["train_non_gpu_count"] == 2
        assert summary["test_gpu_count"] == 1
        assert summary["test_non_gpu_count"] == 1
        assert summary["train_gpu_ratio"] == 0.6  # 3/5
        assert summary["test_gpu_ratio"] == 0.5  # 1/2

    def test_get_split_summary_all_gpu(self):
        """Test split summary with all GPU samples."""
        train_df = pd.DataFrame({"title": ["GPU1", "GPU2"], "bulk_notes": ["Desc1", "Desc2"], "is_gpu": [1, 1]})

        test_df = pd.DataFrame({"title": ["GPU3"], "bulk_notes": ["Desc3"], "is_gpu": [1]})

        summary = get_split_summary(train_df, test_df)

        assert summary["train_gpu_count"] == 2
        assert summary["train_non_gpu_count"] == 0
        assert summary["test_gpu_count"] == 1
        assert summary["test_non_gpu_count"] == 0
        assert summary["train_gpu_ratio"] == 1.0
        assert summary["test_gpu_ratio"] == 1.0

    def test_get_split_summary_no_gpu(self):
        """Test split summary with no GPU samples."""
        train_df = pd.DataFrame({"title": ["NonGPU1", "NonGPU2"], "bulk_notes": ["Desc1", "Desc2"], "is_gpu": [0, 0]})

        test_df = pd.DataFrame({"title": ["NonGPU3"], "bulk_notes": ["Desc3"], "is_gpu": [0]})

        summary = get_split_summary(train_df, test_df)

        assert summary["train_gpu_count"] == 0
        assert summary["train_non_gpu_count"] == 2
        assert summary["test_gpu_count"] == 0
        assert summary["test_non_gpu_count"] == 1
        assert summary["train_gpu_ratio"] == 0.0
        assert summary["test_gpu_ratio"] == 0.0
