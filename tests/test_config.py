# tests/test_config.py
"""Tests for src/config.py module."""

from src.config import (
    CONTEXT_DATA,
    COUNTRIES,
    COUNTRY_RECOMMENDATIONS,
    DATA_EXTERNAL_PATH,
    DATA_PROCESSED_PATH,
    DATA_RAW_PATH,
    DEFAULT_WEIGHTS,
    INDICATORS,
    INDICATORS_DICT,
)


class TestCountries:
    """Tests for COUNTRIES constant."""

    def test_countries_is_non_empty_list(self):
        """COUNTRIES should be a non-empty list."""
        assert isinstance(COUNTRIES, list)
        assert len(COUNTRIES) > 0

    def test_countries_contains_expected_countries(self):
        """COUNTRIES should contain expected European and Asian countries."""
        expected = ["Germany", "Spain", "Norway", "Sweden", "Japan"]
        for country in expected:
            assert country in COUNTRIES


class TestIndicatorsDict:
    """Tests for INDICATORS_DICT constant."""

    def test_indicators_dict_is_dict(self):
        """INDICATORS_DICT should be a dictionary."""
        assert isinstance(INDICATORS_DICT, dict)

    def test_indicators_dict_has_expected_keys(self):
        """INDICATORS_DICT should have expected keys (as file names)."""
        expected_values = ["gdp_per_capita", "gini_index", "education_spending_gdp"]
        for value in expected_values:
            assert value in INDICATORS_DICT.values()


class TestIndicators:
    """Tests for INDICATORS constant."""

    def test_indicators_is_list(self):
        """INDICATORS should be a list."""
        assert isinstance(INDICATORS, list)

    def test_indicators_not_empty(self):
        """INDICATORS should not be empty."""
        assert len(INDICATORS) > 0


class TestContextData:
    """Tests for CONTEXT_DATA constant."""

    def test_context_data_is_dict(self):
        """CONTEXT_DATA should be a dictionary."""
        assert isinstance(CONTEXT_DATA, dict)

    def test_context_data_has_country_key(self):
        """CONTEXT_DATA should have 'country' key."""
        assert "country" in CONTEXT_DATA

    def test_context_data_has_maternity_score_key(self):
        """CONTEXT_DATA should have 'maternity_score' key."""
        assert "maternity_score" in CONTEXT_DATA


class TestDefaultWeights:
    """Tests for DEFAULT_WEIGHTS constant."""

    def test_default_weights_is_dict(self):
        """DEFAULT_WEIGHTS should be a dictionary."""
        assert isinstance(DEFAULT_WEIGHTS, dict)

    def test_default_weights_values_between_0_and_1(self):
        """All weight values should be between 0 and 1."""
        for key, value in DEFAULT_WEIGHTS.items():
            assert 0 <= value <= 1, f"Weight '{key}' value {value} not in range [0, 1]"

    def test_default_weights_sum_equals_1(self):
        """Sum of all weights should equal 1.0."""
        total = sum(DEFAULT_WEIGHTS.values())
        assert abs(total - 1.0) < 1e-6, f"Weights sum {total} != 1.0"


class TestDataPaths:
    """Tests for DATA_*_PATH constants."""

    def test_data_raw_path_is_non_empty_string(self):
        """DATA_RAW_PATH should be a non-empty string."""
        assert isinstance(DATA_RAW_PATH, str)
        assert len(DATA_RAW_PATH) > 0

    def test_data_external_path_is_non_empty_string(self):
        """DATA_EXTERNAL_PATH should be a non-empty string."""
        assert isinstance(DATA_EXTERNAL_PATH, str)
        assert len(DATA_EXTERNAL_PATH) > 0

    def test_data_processed_path_is_non_empty_string(self):
        """DATA_PROCESSED_PATH should be a non-empty string."""
        assert isinstance(DATA_PROCESSED_PATH, str)
        assert len(DATA_PROCESSED_PATH) > 0


class TestCountryRecommendations:
    """Tests for COUNTRY_RECOMMENDATIONS constant."""

    def test_country_recommendations_is_dict(self):
        """COUNTRY_RECOMMENDATIONS should be a dictionary."""
        assert isinstance(COUNTRY_RECOMMENDATIONS, dict)

    def test_country_recommendations_has_entries_for_countries(self):
        """COUNTRY_RECOMMENDATIONS should have entries for countries in COUNTRIES."""
        for country in COUNTRIES:
            if country in COUNTRY_RECOMMENDATIONS:
                # Country exists and has a non-empty recommendation
                assert isinstance(COUNTRY_RECOMMENDATIONS[country], str)
                assert len(COUNTRY_RECOMMENDATIONS[country]) > 0
