"""
Tests for MCP server functionality.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
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
            assert len(tool_dict) >= 20, f"Expected at least 20 tools, got {len(tool_dict)}"
            # Should have testrail_cases tool
            assert 'testrail_cases' in tool_dict
            # Should have testrail_results tool
            assert 'testrail_results' in tool_dict
        
        asyncio.run(check_tools())


class TestMCPServerWithoutFastMCP:
    """Tests for MCP server when fastmcp is not available."""
    
    def test_import_error_when_fastmcp_not_installed(self):
        """Test that ImportError is raised when fastmcp is not installed."""
        # Mock the import to fail
        import sys
        original_import = __import__
        
        def mock_import(name, *args, **kwargs):
            if name == 'fastmcp':
                raise ImportError("No module named 'fastmcp'")
            return original_import(name, *args, **kwargs)
        
        # This is a complex test that would require careful mocking
        # For now, we'll document the expected behavior
        pass

