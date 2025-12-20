#!/usr/bin/env python3
"""Simulate MCP tool call to find JSON issue."""
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
    """Test MCP tool call format."""
    tools = dict(await mcp.get_tools())
    runs_tool = tools.get('testrail_runs')
    
    if runs_tool:
        # Get MCP tool format
        mcp_tool = runs_tool.to_mcp_tool()
        
        # Simulate what Cursor would send
        call_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "testrail_runs",
                "arguments": {
                    "action": "get_runs",
                    "params": {"project_id": 3}
                }
            }
        }
        
        # Try to serialize the request
        try:
            request_json = json.dumps(call_request, indent=2)
            print("✓ Call request is valid JSON")
            print(f"Request length: {len(request_json)}")
            
            # Check position 36
            if len(request_json) > 36:
                print(f"Char at position 36: {repr(request_json[36])}")
                print(f"Context: {repr(request_json[30:50])}")
        except Exception as e:
            print(f"✗ Error serializing request: {e}")
        
        # Try to serialize the tool definition
        try:
            tool_def = {
                "name": mcp_tool.name,
                "description": mcp_tool.description,
                "inputSchema": mcp_tool.inputSchema if hasattr(mcp_tool, 'inputSchema') else mcp_tool.input
            }
            tool_json = json.dumps(tool_def, indent=2)
            print(f"\n✓ Tool definition is valid JSON ({len(tool_json)} chars)")
            
            # Check position 36
            if len(tool_json) > 36:
                print(f"Char at position 36: {repr(tool_json[36])}")
                print(f"Context: {repr(tool_json[30:50])}")
        except Exception as e:
            print(f"\n✗ Error serializing tool: {e}")
            import traceback
            traceback.print_exc()

asyncio.run(test())
