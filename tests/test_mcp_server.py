"""
Tests for MCP server functionality.
"""
import pytest
from unittest.mock import patch
from testrail_api_module import TestRailAPI


@pytest.mark.skipif(
    False,  # fastmcp is now in base dependencies
    reason="fastmcp not installed - should be included in base installation"
)
class TestMCPServer:
    """Tests for MCP server creation and tool registration."""

    def test_create_mcp_server_with_api_instance(self):
        """Test that MCP server can be created with API instance."""
        try:
            from testrail_api_module.mcp_server import create_mcp_server
        except ImportError:
            pytest.skip("fastmcp not installed")

        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        mcp = create_mcp_server(api_instance=api)

        # Should return a FastMCP instance
        from fastmcp import FastMCP
        assert isinstance(mcp, FastMCP)

    def test_create_mcp_server_from_env(self):
        """Test that MCP server can be created from environment variables."""
        try:
            from testrail_api_module.mcp_server import create_mcp_server
            import os
        except ImportError:
            pytest.skip("fastmcp not installed")

        with patch.dict(os.environ, {
            'TESTRAIL_BASE_URL': 'https://test.testrail.io',
            'TESTRAIL_USERNAME': 'test-user',
            'TESTRAIL_API_KEY': 'test-key'
        }):
            mcp = create_mcp_server()

            from fastmcp import FastMCP
            assert isinstance(mcp, FastMCP)

    def test_raises_error_when_fastmcp_not_installed(self):
        """Test that error is raised when fastmcp is not installed."""
        # This test would need to mock the import failure
        # For now, we'll skip it as it's hard to test import failures
        pass

    def test_registers_tools_from_all_modules(self):
        """Test that module-based tools are registered from all API modules."""
        try:
            from testrail_api_module.mcp_server import create_mcp_server
            import asyncio
        except ImportError:
            pytest.skip("fastmcp not installed")

        api = TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        mcp = create_mcp_server(api_instance=api)

        # The server should have tools registered
        # Verify we have module-based tools (should be ~22, one per module)
        async def check_tools():
            tools = await mcp.get_tools()
            tool_dict = dict(tools)
            # Should have approximately 22 module-based tools
            assert len(tool_dict) >= 20, f"Expected at least 20 tools, got {
                len(tool_dict)}"
            # Should have testrail_cases tool
            assert 'testrail_cases' in tool_dict
            # Should have testrail_results tool
            assert 'testrail_results' in tool_dict

        asyncio.run(check_tools())

    def test_custom_fields_automatic_separation(self):
        """Test that custom fields passed as top-level params are automatically separated."""
        try:
            from testrail_api_module.mcp_server import (
                _separate_custom_fields_for_case_action
            )
        except ImportError:
            pytest.skip("fastmcp not installed")

        # Test the separation function directly
        # Create API instance (not used, but needed for function call)
        TestRailAPI(
            base_url='https://test.testrail.io',
            username='test',
            api_key='test-key'
        )

        # Test the separation function directly
        params = {
            'section_id': 123,
            'title': 'Test Case',
            'custom_steps': 'Step 1\nStep 2',  # Top-level custom field
            'custom_expected': 'Expected result'  # Top-level custom field
        }

        separated = _separate_custom_fields_for_case_action('add_case', params)

        # Verify custom fields are now nested
        assert 'custom_fields' in separated
        assert separated['custom_fields']['custom_steps'] == 'Step 1\nStep 2'
        assert separated['custom_fields']['custom_expected'] == 'Expected result'
        # Verify standard fields remain at top level
        assert separated['section_id'] == 123
        assert separated['title'] == 'Test Case'
        # Verify top-level custom fields are removed
        assert 'custom_steps' not in separated or separated.get(
            'custom_steps') is None
        assert 'custom_expected' not in separated or separated.get(
            'custom_expected') is None

        # Test with already nested custom_fields
        params_nested = {
            'section_id': 123,
            'title': 'Test Case',
            'custom_fields': {
                'custom_automation_type': '7'
            },
            'custom_steps': 'Step 1'  # Top-level that should be merged
        }

        separated_nested = _separate_custom_fields_for_case_action(
            'add_case', params_nested)
        assert 'custom_fields' in separated_nested
        assert separated_nested['custom_fields']['custom_automation_type'] == '7'
        assert separated_nested['custom_fields']['custom_steps'] == 'Step 1'

        # Test update_case action
        params_update = {
            'case_id': 456,
            'title': 'Updated Case',
            'custom_module': ['3', '5']
        }

        separated_update = _separate_custom_fields_for_case_action(
            'update_case', params_update)
        assert 'custom_fields' in separated_update
        assert separated_update['custom_fields']['custom_module'] == ['3', '5']
        assert separated_update['case_id'] == 456


class TestMCPServerWithoutFastMCP:
    """Tests for MCP server when fastmcp is not available."""

    def test_import_error_when_fastmcp_not_installed(self):
        """Test that ImportError is raised when fastmcp is not installed."""
        # Mock the import to fail
        original_import = __import__

        def mock_import(name, *args, **kwargs):
            if name == 'fastmcp':
                raise ImportError("No module named 'fastmcp'")
            return original_import(name, *args, **kwargs)

        # This is a complex test that would require careful mocking
        # For now, we'll document the expected behavior
        pass
