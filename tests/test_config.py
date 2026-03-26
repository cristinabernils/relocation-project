# tests/test_config.py
"""Tests for src/config.py"""

import pandas as pd

from src.config import (
    CONTEXT_DATA,
    COUNTRIES,
    COUNTRY_RECOMMENDATIONS,
    DEFAULT_WEIGHTS,
    INDICATORS_DICT,
)


class TestConfig:
    """Test suite for centralized configuration."""

    def test_countries_not_empty(self):
        """Countries list should not be empty."""
        assert len(COUNTRIES) > 0

    def test_countries_are_valid_codes(self):
        """All countries should be valid ISO codes."""
        for code in COUNTRIES:
            assert isinstance(code, str)
            assert len(code) == 3
            assert code.isupper()

    def test_indicators_dict_has_required_keys(self):
        """Should have all required World Bank indicators."""
        required = ["gdp_per_capita", "gini_index", "unemployment"]
        for indicator in required:
            assert indicator in INDICATORS_DICT.values()

    def test_context_data_structure(self):
        """CONTEXT_DATA should have country and maternity_score."""
        assert "country" in CONTEXT_DATA
        assert "maternity_score" in CONTEXT_DATA
        assert len(CONTEXT_DATA["country"]) == len(CONTEXT_DATA["maternity_score"])

    def test_maternity_scores_in_range(self):
        """Maternity scores should be between 1 and 5."""
        for score in CONTEXT_DATA["maternity_score"]:
            assert 1 <= score <= 5

    def test_weights_sum_to_one(self):
        """Weights should sum to 1.0 (normalized)."""
        total = sum(DEFAULT_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001

    def test_all_countries_have_recommendations(self):
        """All countries in CONTEXT_DATA should have a recommendation."""
        for country in CONTEXT_DATA["country"]:
            assert country in COUNTRY_RECOMMENDATIONS
            assert len(COUNTRY_RECOMMENDATIONS[country]) > 0

    def test_context_data_dataframe_creation(self):
        """Should be able to create a valid DataFrame from CONTEXT_DATA."""
        df = pd.DataFrame(CONTEXT_DATA)
        assert not df.empty
        assert "country" in df.columns
        assert "maternity_score" in df.columns
