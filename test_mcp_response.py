#!/usr/bin/env python3
"""Test MCP tools/list response format."""
import json
from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_server import create_mcp_server
import asyncio

api = TestRailAPI(
    base_url='https://your-instance.testrail.io',
    username='your-username@example.com',
    api_key='your-api-key-here'
)

mcp = create_mcp_server(api_instance=api)

async def test():
    """Test MCP response format."""
    # This simulates what FastMCP sends in tools/list response
    tools = await mcp.get_tools()
    
    # Convert to MCP format
    tools_dict = dict(tools)
    mcp_tools = []
    for name, tool in tools_dict.items():
        mcp_tool = tool.to_mcp_tool()
        tool_dict = {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "inputSchema": mcp_tool.inputSchema if hasattr(mcp_tool, 'inputSchema') else mcp_tool.input
        }
        mcp_tools.append(tool_dict)
    
    # MCP tools/list response format
    response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": mcp_tools
        }
    }
    
    # Try to serialize
    try:
        response_json = json.dumps(response, indent=2)
        print(f"✓ Response is valid JSON ({len(response_json)} chars)")
        
        # Check position 36
        if len(response_json) > 36:
            print(f"Char at position 36: {repr(response_json[36])}")
            print(f"Context: {repr(response_json[30:50])}")
            
        # Try to parse it back
        parsed = json.loads(response_json)
        print("✓ Response can be parsed back")
        
        # Check the runs tool specifically
        runs_tool = None
        for tool in mcp_tools:
            if tool['name'] == 'testrail_runs':
                runs_tool = tool
                break
        
        if runs_tool:
            runs_json = json.dumps(runs_tool, indent=2)
            print(f"\n✓ testrail_runs tool is valid JSON ({len(runs_json)} chars)")
            if len(runs_json) > 36:
                print(f"Char at position 36: {repr(runs_json[36])}")
                print(f"Context: {repr(runs_json[30:50])}")
    except json.JSONDecodeError as e:
        print(f"✗ JSON error: {e}")
        print(f"At position: {e.pos}")
        if e.pos > 0:
            start = max(0, e.pos - 20)
            end = min(len(response_json), e.pos + 20)
            print(f"Context: {repr(response_json[start:end])}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
