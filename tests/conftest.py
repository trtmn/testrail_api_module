"""Shared fixtures for the test suite.

Fixtures that are identical across module test files live here so there is
one definition to maintain. Module-specific variants stay local and
override these (pytest resolves the closest fixture first).
"""

from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_client() -> Mock:
    """Create a mock TestRail client."""
    client = Mock()
    client.base_url = "https://testrail.example.com"
    client.username = "testuser"
    client.api_key = "test_api_key"
    return client
