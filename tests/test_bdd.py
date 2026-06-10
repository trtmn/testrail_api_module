"""
Tests for the BDDAPI module.

This module contains comprehensive tests for all methods in the BDDAPI class,
including edge cases, error handling, and proper API request formatting.
"""

from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest

from testrail_api_module.base import (
    TestRailAPIError,
    TestRailAuthenticationError,
    TestRailRateLimitError,
)
from testrail_api_module.bdd import BDDAPI

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture  # noqa: F401


class TestBDDAPI:
    """Test suite for BDDAPI class."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock TestRail client."""
        client = Mock()
        client.base_url = "https://testrail.example.com"
        client.username = "testuser"
        client.api_key = "test_api_key"
        return client

    @pytest.fixture
    def bdd_api(self, mock_client: Mock) -> BDDAPI:
        """Create a BDDAPI instance with mocked client."""
        return BDDAPI(mock_client)

    @pytest.fixture
    def sample_case_data(self) -> dict:
        """Sample test case data returned by add_bdd."""
        return {
            "id": 2136,
            "title": "Users cannot login with invalid credentials",
            "section_id": 188,
        }

    def test_init(self, mock_client: Mock) -> None:
        """Test BDDAPI initialization."""
        api = BDDAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, "logger")

    def test_get_bdd(self, bdd_api: BDDAPI) -> None:
        """Test get_bdd downloads the raw .feature file content."""
        with patch.object(bdd_api, "_get") as mock_get:
            mock_get.return_value = b"Feature: Test Feature"

            result = bdd_api.get_bdd(case_id=1)

            mock_get.assert_called_once_with("get_bdd/1", raw=True)
            assert result == b"Feature: Test Feature"

    def test_add_bdd(self, bdd_api: BDDAPI, sample_case_data: dict) -> None:
        """Test add_bdd uploads the .feature file via multipart."""
        with patch.object(bdd_api, "_post_multipart") as mock_multipart:
            mock_multipart.return_value = sample_case_data

            result = bdd_api.add_bdd(
                section_id=188, feature_file="/path/to/feature.feature"
            )

            mock_multipart.assert_called_once_with(
                "add_bdd/188", "/path/to/feature.feature"
            )
            assert result == sample_case_data

    def test_add_bdd_file_not_found(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd when file is not found."""
        with patch.object(bdd_api, "_post_multipart") as mock_multipart:
            mock_multipart.side_effect = FileNotFoundError("missing")

            with pytest.raises(
                FileNotFoundError, match="Feature file not found"
            ):
                bdd_api.add_bdd(
                    section_id=1, feature_file="/nonexistent/feature.feature"
                )

    def test_api_request_failure(self, bdd_api: BDDAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(bdd_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAPIError("API request failed")

            with pytest.raises(TestRailAPIError, match="API request failed"):
                bdd_api.get_bdd(case_id=1)

    def test_authentication_error(self, bdd_api: BDDAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(bdd_api, "_get") as mock_get:
            mock_get.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                bdd_api.get_bdd(case_id=1)

    def test_rate_limit_error(self, bdd_api: BDDAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(bdd_api, "_get") as mock_get:
            mock_get.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                bdd_api.get_bdd(case_id=1)

    def test_add_bdd_authentication_error(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd propagates authentication errors."""
        with patch.object(bdd_api, "_post_multipart") as mock_multipart:
            mock_multipart.side_effect = TestRailAuthenticationError(
                "Authentication failed"
            )

            with pytest.raises(
                TestRailAuthenticationError, match="Authentication failed"
            ):
                bdd_api.add_bdd(
                    section_id=1, feature_file="/path/to/feature.feature"
                )

    def test_add_bdd_rate_limit_error(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd propagates rate limit errors."""
        with patch.object(bdd_api, "_post_multipart") as mock_multipart:
            mock_multipart.side_effect = TestRailRateLimitError(
                "Rate limit exceeded"
            )

            with pytest.raises(
                TestRailRateLimitError, match="Rate limit exceeded"
            ):
                bdd_api.add_bdd(
                    section_id=1, feature_file="/path/to/feature.feature"
                )
