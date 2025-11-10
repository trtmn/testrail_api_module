"""
Tests for the BDDAPI module.

This module contains comprehensive tests for all methods in the BDDAPI class,
including edge cases, error handling, and proper API request formatting.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from typing import TYPE_CHECKING

from testrail_api_module.bdd import BDDAPI
from testrail_api_module.base import TestRailAPIError, TestRailAuthenticationError, TestRailRateLimitError

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


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

    def test_init(self, mock_client: Mock) -> None:
        """Test BDDAPI initialization."""
        api = BDDAPI(mock_client)
        assert api.client == mock_client
        assert hasattr(api, 'logger')

    def test_get_bdd(self, bdd_api: BDDAPI) -> None:
        """Test get_bdd method."""
        with patch.object(bdd_api, '_api_request') as mock_request:
            mock_request.return_value = {
                "feature": "Feature: Test Feature",
                "scenarios": []
            }
            
            result = bdd_api.get_bdd(case_id=1)
            
            mock_request.assert_called_once_with('GET', 'get_bdd/1')
            assert "feature" in result

    def test_add_bdd_minimal(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd with minimal required parameters."""
        with patch.object(bdd_api, '_api_request') as mock_request, \
             patch('builtins.open', mock_open(read_data="Feature: Test Feature")):
            mock_request.return_value = {"id": 1, "feature": "Test Feature"}
            
            result = bdd_api.add_bdd(
                section_id=1,
                feature_file="/path/to/feature.feature"
            )
            
            expected_data = {"file": "Feature: Test Feature"}
            mock_request.assert_called_once_with('POST', 'add_bdd/1', expected_data)
            assert result == {"id": 1, "feature": "Test Feature"}

    def test_add_bdd_with_description(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd with description."""
        with patch.object(bdd_api, '_api_request') as mock_request, \
             patch('builtins.open', mock_open(read_data="Feature: Test Feature")):
            mock_request.return_value = {"id": 1}
            
            result = bdd_api.add_bdd(
                section_id=1,
                feature_file="/path/to/feature.feature",
                description="Feature description"
            )
            
            expected_data = {
                "file": "Feature: Test Feature",
                "description": "Feature description"
            }
            mock_request.assert_called_once_with('POST', 'add_bdd/1', expected_data)

    def test_add_bdd_file_not_found(self, bdd_api: BDDAPI) -> None:
        """Test add_bdd when file is not found."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError, match="Feature file not found"):
                bdd_api.add_bdd(
                    section_id=1,
                    feature_file="/nonexistent/feature.feature"
                )

    def test_api_request_failure(self, bdd_api: BDDAPI) -> None:
        """Test behavior when API request fails."""
        with patch.object(bdd_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAPIError("API request failed")
            
            with pytest.raises(TestRailAPIError, match="API request failed"):
                bdd_api.get_bdd(case_id=1)

    def test_authentication_error(self, bdd_api: BDDAPI) -> None:
        """Test behavior when authentication fails."""
        with patch.object(bdd_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailAuthenticationError("Authentication failed")
            
            with pytest.raises(TestRailAuthenticationError, match="Authentication failed"):
                bdd_api.get_bdd(case_id=1)

    def test_rate_limit_error(self, bdd_api: BDDAPI) -> None:
        """Test behavior when rate limit is exceeded."""
        with patch.object(bdd_api, '_api_request') as mock_request:
            mock_request.side_effect = TestRailRateLimitError("Rate limit exceeded")
            
            with pytest.raises(TestRailRateLimitError, match="Rate limit exceeded"):
                bdd_api.get_bdd(case_id=1)





