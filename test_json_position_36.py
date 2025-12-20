#!/usr/bin/env python3
"""Test what's at position 36 in MCP protocol messages."""
import json
import asyncio
from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_server import create_mcp_server

api = TestRailAPI(
    base_url='https://your-instance.testrail.io',
    username='your-username@example.com',
    api_key='your-api-key-here'
)

mcp = create_mcp_server(api_instance=api)

async def test():
    """Test MCP protocol message format."""
    # Simulate tools/list response
    tools_dict = dict(await mcp.get_tools())
    tools_list = []
    
    for name, tool in tools_dict.items():
        mcp_tool = tool.to_mcp_tool()
        tool_dict = {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "inputSchema": mcp_tool.inputSchema if hasattr(mcp_tool, 'inputSchema') else mcp_tool.input
        }
        tools_list.append(tool_dict)
    
    # MCP tools/list response
    response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": tools_list
        }
    }
    
    json_str = json.dumps(response)
    print(f"Full response JSON length: {len(json_str)}")
    print(f"Char at position 36: {repr(json_str[36])}")
    print(f"Context (20-60): {repr(json_str[20:60])}")
    print(f"\nFirst 100 chars: {json_str[:100]}")
    
    # Check if it's valid
    try:
        json.loads(json_str)
        print("\n✓ JSON is valid")
    except json.JSONDecodeError as e:
        print(f"\n✗ JSON error at {e.pos}: {e.msg}")

asyncio.run(test())
