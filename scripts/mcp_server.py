#!/usr/bin/env python3
"""
Command-line interface for running the TestRail API MCP server.

This script starts an MCP server that exposes all TestRail API methods
as MCP tools.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from testrail_api_module import TestRailAPI
    from testrail_api_module.mcp_server import create_mcp_server
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
    
    Args:
        env_file: Path to the .env file.
    """
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
    except ImportError:
        # python-dotenv is optional
        pass


def setup_logging(verbose: bool = False) -> None:
    """
    Set up logging configuration.
    
    Args:
        verbose: If True, set log level to DEBUG.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
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
    
    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Load .env file if specified or if .env exists in current directory
    env_file = args.env_file or '.env'
    if os.path.exists(env_file):
        load_env_file(env_file)
        logger.debug(f"Loaded environment variables from {env_file}")
    
    # Get configuration from args or environment
    base_url = args.base_url or os.getenv('TESTRAIL_BASE_URL')
    username = args.username or os.getenv('TESTRAIL_USERNAME')
    api_key = args.api_key or os.getenv('TESTRAIL_API_KEY')
    password = args.password or os.getenv('TESTRAIL_PASSWORD')
    timeout = args.timeout or int(os.getenv('TESTRAIL_TIMEOUT', '30'))
    
    # Validate required parameters
    if not base_url:
        logger.error("TESTRAIL_BASE_URL is required (use --base-url or set env var)")
        sys.exit(1)
    
    if not username:
        logger.error("TESTRAIL_USERNAME is required (use --username or set env var)")
        sys.exit(1)
    
    if not api_key and not password:
        logger.error(
            "Either TESTRAIL_API_KEY or TESTRAIL_PASSWORD is required "
            "(use --api-key/--password or set env var)"
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
        logger.info("TestRail API client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize TestRail API client: {e}")
        sys.exit(1)
    
    # Create and run MCP server
    try:
        mcp = create_mcp_server(api_instance=api, server_name=args.server_name)
        logger.info(f"Starting MCP server: {args.server_name}")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error running MCP server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

