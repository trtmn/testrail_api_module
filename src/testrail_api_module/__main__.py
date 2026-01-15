"""
Entry point for running the package as a module.

This allows the package to be run directly with:
    python -m testrail_api_module
    uvx testrail-api-module

Both commands will start the MCP server.
"""
from .cli import main

if __name__ == "__main__":
    main()
