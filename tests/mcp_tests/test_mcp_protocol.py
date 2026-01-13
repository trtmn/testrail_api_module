#!/usr/bin/env python3
"""Test the actual MCP protocol communication."""
import json
import asyncio
from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_server import create_mcp_server

api = TestRailAPI(
    base_url='https://your-instance.testrail.io',
    username='your-username',
    api_key='your-api-key'
)

mcp = create_mcp_server(api_instance=api)

async def test():
    """Test MCP protocol."""
    # Get tools and try to serialize them
    tools_dict = dict(await mcp.get_tools())
    
    # Try to serialize all tools to see if any cause JSON issues
    for name, tool in list(tools_dict.items())[:5]:  # Test first 5
        try:
            mcp_tool = tool.to_mcp_tool()
            # Try to serialize the tool as it would be in MCP protocol
            tool_dict = {
                'name': mcp_tool.name,
                'description': mcp_tool.description,
                'inputSchema': mcp_tool.inputSchema if hasattr(mcp_tool, 'inputSchema') else mcp_tool.input
            }
            json_str = json.dumps(tool_dict, indent=2)
            # Check position 37
            if len(json_str) > 37:
                char_at_37 = json_str[37]
                print(f'{name}: char at 37 = {repr(char_at_37)}, context = {repr(json_str[30:50])}')
        except Exception as e:
            print(f'{name}: Error - {e}')
            import traceback
            traceback.print_exc()

asyncio.run(test())

