from . import TestRailAPI as TestRailAPI
from .mcp_server import create_mcp_server as create_mcp_server
from pathlib import Path as Path

def load_env_file(env_file: str) -> None:
    """
    Load environment variables from a .env file.
    
    This function uses python-dotenv to load environment variables from
    a .env file. If python-dotenv is not installed, this function silently
    does nothing (it's an optional dependency).
    
    Args:
        env_file: Path to the .env file to load.
        
    Note:
        This function will not raise an error if python-dotenv is not
        installed, making it safe to call even when the dependency is
        optional.
    """
def setup_logging(verbose: bool = False, debug: bool = False) -> None:
    """
    Set up logging configuration for the CLI.
    
    Configures Python's logging module with appropriate format and level.
    When verbose or debug is True, DEBUG level logging is enabled for detailed
    information about tool registration and API calls.
    
    For MCP servers running in stdio mode, logging is disabled by default
    to avoid interfering with stdio communication. Use --verbose or set
    TESTRAIL_MCP_DEBUG=1 only for debugging.
    
    Args:
        verbose: If True, set log level to DEBUG. Otherwise, logging is
                 disabled to avoid interfering with stdio communication.
        debug: If True, enable debug logging. This can be set via the
               TESTRAIL_MCP_DEBUG environment variable.
        
    Note:
        This function configures logging to show only TestRail MCP debug
        messages, not FastMCP's internal debug logs.
    """
def main() -> None:
    """
    Main entry point for the CLI.
    
    This function parses command-line arguments, loads configuration from
    environment variables or .env files, validates the configuration, creates
    a TestRailAPI instance, and starts the MCP server.
    
    The function handles:
    - Command-line argument parsing
    - Environment variable loading
    - Configuration validation
    - API client initialization
    - MCP server creation and startup
    - Error handling and logging
    
    Exits with code 0 on success, 1 on error.
    
    Raises:
        SystemExit: Always exits (either 0 or 1), never returns normally.
    """
