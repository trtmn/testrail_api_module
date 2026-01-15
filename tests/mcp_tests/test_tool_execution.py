#!/usr/bin/env python3
"""Test actual tool execution."""
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
    """Test tool execution."""
    tools_dict = dict(await mcp.get_tools())
    runs_tool = tools_dict.get('testrail_runs')
    
    if runs_tool:
        print('Testing testrail_runs tool execution...')
        try:
            # Get the function
            fn = runs_tool.fn
            # Call it directly
            result = fn(action='get_runs', params={'project_id': 3})
            print(f'Success! Got {len(result)} runs')
            if result:
                print(f'First run: {result[0].get("name", "N/A")} (ID: {result[0].get("id", "N/A")})')
        except Exception as e:
            print(f'Error executing tool: {e}')
            import traceback
            traceback.print_exc()
    else:
        print('testrail_runs tool not found')

asyncio.run(test())

