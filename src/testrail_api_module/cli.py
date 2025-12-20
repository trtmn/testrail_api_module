"""
Command-line interface for running the TestRail API MCP server.

This module provides the CLI entry point for the MCP server, allowing users
to start the server from the command line with various configuration options.

The CLI supports configuration via:
- Command-line arguments (highest priority)
- Environment variables
- .env files

Example:
    # Using environment variables
    export TESTRAIL_BASE_URL="https://test.testrail.io"
    export TESTRAIL_USERNAME="user@example.com"
    export TESTRAIL_API_KEY="api-key-123"
    testrail-mcp-server
    
    # Using command-line arguments
    testrail-mcp-server \\
      --base-url "https://test.testrail.io" \\
      --username "user@example.com" \\
      --api-key "api-key-123" \\
      --verbose
"""
import logging
import os
import sys
from pathlib import Path

try:
    from . import TestRailAPI
    from .mcp_server import create_mcp_server
except ImportError as e:
    print(f"Error importing testrail_api_module: {e}", file=sys.stderr)
    print(
        "Make sure testrail-api-module is installed and fastmcp is available.",
        file=sys.stderr
    )
    print(
        "Install with: pip install testrail-api-module",
        file=sys.stderr
    )
    sys.exit(1)


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
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # python-dotenv is optional
        pass


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration for the CLI.
    
    Configures Python's logging module with appropriate format and level.
    When verbose is True, DEBUG level logging is enabled for detailed
    information about tool registration and API calls.
    
    For MCP servers running in stdio mode, logging is disabled by default
    to avoid interfering with stdio communication. Use --verbose only for
    debugging.
    
    Args:
        verbose: If True, set log level to DEBUG. Otherwise, logging is
                 disabled to avoid interfering with stdio communication.
        
    Note:
        This function configures the root logger, so it affects all
        loggers in the application.
    """
    if verbose:
        level = logging.DEBUG
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # Disable all logging in stdio mode to avoid interfering with MCP communication
        # This includes FastMCP's internal logging
        logging.disable(logging.CRITICAL)
        # Also set log level to ERROR for all loggers
        logging.getLogger().setLevel(logging.ERROR)
        # Specifically disable FastMCP logging
        logging.getLogger('fastmcp').setLevel(logging.ERROR)
        logging.getLogger('uvicorn').setLevel(logging.ERROR)


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
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Start TestRail API MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use environment variables
  export TESTRAIL_BASE_URL="https://your-instance.testrail.io"
  export TESTRAIL_USERNAME="your-username"
  export TESTRAIL_API_KEY="your-api-key"
  testrail-mcp-server

  # Use command-line arguments
  testrail-mcp-server \\
    --base-url "https://your-instance.testrail.io" \\
    --username "your-username" \\
    --api-key "your-api-key"

  # Use .env file
  testrail-mcp-server --env-file .env

  # Verbose logging
  testrail-mcp-server --verbose
        """
    )
    
    parser.add_argument(
        '--base-url',
        type=str,
        help='TestRail base URL (or set TESTRAIL_BASE_URL env var)'
    )
    parser.add_argument(
        '--username',
        type=str,
        help='TestRail username (or set TESTRAIL_USERNAME env var)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='TestRail API key (or set TESTRAIL_API_KEY env var)'
    )
    parser.add_argument(
        '--password',
        type=str,
        help='TestRail password (or set TESTRAIL_PASSWORD env var)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--env-file',
        type=str,
        help='Path to .env file (default: .env in current directory)'
    )
    parser.add_argument(
        '--server-name',
        type=str,
        default='TestRail API Server',
        help='Name for the MCP server (default: TestRail API Server)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Suppress FastMCP and uvicorn logging in non-verbose mode
    if not args.verbose:
        import os
        os.environ.setdefault('LOG_LEVEL', 'ERROR')
        os.environ.setdefault('UVICORN_LOG_LEVEL', 'error')
    
    # Load .env file if specified or if .env exists in current directory
    env_file = args.env_file or '.env'
    if os.path.exists(env_file):
        load_env_file(env_file)
        if args.verbose:
            logger.debug(f"Loaded environment variables from {env_file}")
    
    # Get configuration from args or environment
    base_url = args.base_url or os.getenv('TESTRAIL_BASE_URL')
    username = args.username or os.getenv('TESTRAIL_USERNAME')
    api_key = args.api_key or os.getenv('TESTRAIL_API_KEY')
    password = args.password or os.getenv('TESTRAIL_PASSWORD')
    timeout = args.timeout or int(os.getenv('TESTRAIL_TIMEOUT', '30'))
    
    # Validate required parameters
    if not base_url:
        print("ERROR: TESTRAIL_BASE_URL is required (use --base-url or set env var)", file=sys.stderr)
        sys.exit(1)
    
    if not username:
        print("ERROR: TESTRAIL_USERNAME is required (use --username or set env var)", file=sys.stderr)
        sys.exit(1)
    
    if not api_key and not password:
        print(
            "ERROR: Either TESTRAIL_API_KEY or TESTRAIL_PASSWORD is required "
            "(use --api-key/--password or set env var)",
            file=sys.stderr
        )
        sys.exit(1)
    
    # Create API instance
    try:
        api = TestRailAPI(
            base_url=base_url,
            username=username,
            api_key=api_key,
            password=password,
            timeout=timeout
        )
        if args.verbose:
            logger.info("TestRail API client initialized")
    except Exception as e:
        print(f"ERROR: Failed to initialize TestRail API client: {e}", file=sys.stderr)
        if args.verbose:
            logger.error(f"Failed to initialize TestRail API client: {e}", exc_info=True)
        sys.exit(1)
    
    # Create and run MCP server
    try:
        mcp = create_mcp_server(api_instance=api, server_name=args.server_name)
        if args.verbose:
            logger.info(f"Starting MCP server: {args.server_name}")
        # Run the server - this will block and handle stdio communication
        # Disable banner in stdio mode to avoid interfering with MCP protocol
        # Explicitly set transport to stdio for MCP clients
        mcp.run(transport="stdio", show_banner=False)
    except KeyboardInterrupt:
        if args.verbose:
            logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        # Log errors to stderr so they don't interfere with stdio
        print(f"Error running MCP server: {e}", file=sys.stderr)
        if args.verbose:
            logger.error(f"Error running MCP server: {e}", exc_info=True)
        sys.exit(1)

