#!/usr/bin/env python3
"""Test script to inspect the MCP tool schema generation."""
import json
from testrail_api_module import TestRailAPI
from testrail_api_module.mcp_server import create_mcp_server

# Create a dummy API instance
api = TestRailAPI(
    base_url="https://test.testrail.io",
    username="test",
    api_key="test-key"
)

# Create MCP server
mcp = create_mcp_server(api_instance=api)

# Try to get the tools and inspect their schemas


async def inspect_schemas():
    tools = await mcp.get_tools()
    for tool_name, tool in tools:
        print(f"\n=== Tool: {tool_name} ===")
        try:
            # Try to get the schema
            schema = tool.inputSchema
            schema_json = json.dumps(schema, indent=2)
            print("Schema (first 200 chars):")
            print(schema_json[:200])
            # Check position 37
            if len(schema_json) > 37:
                print(f"\nCharacter at position 37: '{schema_json[37]}'")
                print("Context around position 37:")
                start = max(0, 37 - 20)
                end = min(len(schema_json), 37 + 20)
                print(f"  {schema_json[start:end]}")
                print(f"  {' ' * (37 - start)}^")
        except Exception as e:
            print(f"Error inspecting schema: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    import asyncio
    asyncio.run(inspect_schemas())
