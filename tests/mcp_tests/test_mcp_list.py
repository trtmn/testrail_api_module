#!/usr/bin/env python3
"""Test MCP tools/list response."""
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
    """Test MCP tools/list format."""
    # Get all tools
    tools_dict = dict(await mcp.get_tools())
    tools_list = []

    for name, tool in tools_dict.items():
        mcp_tool = tool.to_mcp_tool()
        tool_dict = {
            'name': mcp_tool.name,
            'description': mcp_tool.description,
            'inputSchema': mcp_tool.inputSchema if hasattr(
                mcp_tool,
                'inputSchema') else mcp_tool.input}
        tools_list.append(tool_dict)

    # This is what would be sent in MCP tools/list response
    response = {
        'tools': tools_list
    }

    # Try to serialize it
    try:
        json_str = json.dumps(response, indent=2)
        # Check position 37
        if len(json_str) > 37:
            print(f'Char at position 37: {repr(json_str[37])}')
            print(f'Context: {repr(json_str[30:50])}')
        print(f'\n✓ Full response is valid JSON ({len(json_str)} chars)')

        # Check for any tools with issues
        for i, tool in enumerate(tools_list):
            tool_json = json.dumps(tool, indent=2)
            if len(tool_json) > 37:
                char = tool_json[37]
                if char not in [' ', '\n', '"', '{', '}', ',', ':']:
                    print(
                        f'\nTool {i} ({
                            tool["name"]}) has unusual char at 37: {
                            repr(char)}')
                    print(f'Context: {repr(tool_json[30:50])}')
    except json.JSONDecodeError as e:
        print(f'\n✗ JSON error: {e}')
        print(f'At position: {e.pos}')
        if e.pos > 0:
            print(f'Context: {repr(json_str[max(0, e.pos - 20):e.pos + 20])}')

asyncio.run(test())
