#!/usr/bin/env python3
"""
Script to update the version in the module's __init__.py file.
This script is typically called by bumpversion after updating pyproject.toml.
"""
import re
import sys
from pathlib import Path


def update_version_in_init(project_root: Path, new_version: str) -> None:
    """Update the version in the __init__.py file."""
    init_file = project_root / "src" / "testrail_api_module" / "__init__.py"
    
    if not init_file.exists():
        print(f"❌ Init file not found: {init_file}")
        sys.exit(1)
    
    # Read the current content
    with open(init_file, 'r') as f:
        content = f.read()
    
    # Update the version string
    # Look for the pattern: __version__ = 'x.y.z'
    pattern = r"__version__\s*=\s*['\"]([^'\"]+)['\"]"
    replacement = f"__version__ = '{new_version}'"
    
    if re.search(pattern, content):
        new_content = re.sub(pattern, replacement, content)
        
        # Write the updated content back
        with open(init_file, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated version to {new_version} in {init_file}")
    else:
        print(f"❌ Could not find version pattern in {init_file}")
        sys.exit(1)


def main() -> None:
    """Main function to update version."""
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        print("Example: python update_version.py 0.3.0")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format (simple check)
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print(f"❌ Invalid version format: {new_version}")
        print("Expected format: x.y.z (e.g., 0.3.0)")
        sys.exit(1)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Update the version
    update_version_in_init(project_root, new_version)


if __name__ == "__main__":
    main() 