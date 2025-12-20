#!/usr/bin/env python3
"""Test script to debug the MCP tool schema generation."""
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
    """Test schema generation."""
    try:
        # Get tools
        tools_dict = dict(await mcp.get_tools())
        
        # Find runs tool
        runs_tool = None
        for name, tool in tools_dict.items():
            if 'runs' in name:
                runs_tool = tool
                print(f'Found tool: {name}')
                break
        
        if runs_tool:
            # Try to get MCP tool format
            try:
                mcp_tool = runs_tool.to_mcp_tool()
                print(f'\nMCP Tool format:')
                print(f'Name: {mcp_tool.name}')
                print(f'Description: {mcp_tool.description[:100]}...')
                if hasattr(mcp_tool, 'inputSchema'):
                    schema_str = json.dumps(mcp_tool.inputSchema, indent=2)
                elif hasattr(mcp_tool, 'input'):
                    schema_str = json.dumps(mcp_tool.input, indent=2)
                else:
                    # Try to serialize the whole tool
                    schema_str = json.dumps(mcp_tool.model_dump() if hasattr(mcp_tool, 'model_dump') else str(mcp_tool), indent=2)
            except Exception as e:
                print(f'Error getting MCP tool format: {e}')
                import traceback
                traceback.print_exc()
                return
            print(f'\nSchema length: {len(schema_str)}')
            print(f'\nFirst 200 chars:\n{schema_str[:200]}')
            
            print(f'\nFull schema:\n{schema_str}')
            
            # Try to parse it
            try:
                parsed = json.loads(schema_str)
                print('\n✓ Schema is valid JSON')
                
                # Now try to actually call the tool
                print('\nTesting tool call...')
                result = await mcp.call_tool('testrail_runs', {
                    'action': 'get_runs',
                    'params': {'project_id': 3}
                })
                print(f'Result: {result}')
            except json.JSONDecodeError as e:
                print(f'\n✗ JSON parsing error: {e}')
                print(f'Error at position: {e.pos}')
                if e.pos > 0:
                    start = max(0, e.pos - 20)
                    end = min(len(schema_str), e.pos + 20)
                    print(f'Context: {repr(schema_str[start:end])}')
            except Exception as e:
                print(f'\nError calling tool: {e}')
                import traceback
                traceback.print_exc()
        else:
            print('Runs tool not found')
            print(f'Available tools: {list(tools_dict.keys())}')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test())

