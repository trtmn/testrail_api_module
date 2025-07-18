#!/usr/bin/env python3
"""
Script to generate documentation for the TestRail API module using pdoc.
"""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Generate documentation using pdoc."""
    # Get the project root directory (utilities/../)
    project_root = Path(__file__).parent.parent

    # Remove existing docs directory
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        print("Removing existing docs directory...")
        subprocess.run(["rm", "-rf", str(docs_dir)], check=True)

    # Generate new documentation
    print("Generating documentation with pdoc...")
    try:
        subprocess.run(
            [
                "pdoc",
                "--output-directory",
                str(docs_dir),
                str(project_root / "src" / "testrail_api_module"),
            ],
            check=True,
        )
        print("✅ Documentation generated successfully!")
        print(f"📁 Documentation is available in: {docs_dir}")
        print(
            f"🌐 Open {docs_dir / 'testrail_api_module' / 'index.html'} "
            f"in your browser to view it."
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating documentation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
