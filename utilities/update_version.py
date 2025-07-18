#!/usr/bin/env python3
"""
Script to update the version using bump-my-version.
This script can be used to bump versions in both pyproject.toml and __init__.py files.
"""
import subprocess
import sys
from pathlib import Path


def run_bump_version(project_root: Path, part: str, dry_run: bool = False) -> None:
    """Run bump-my-version to update the version."""
    cmd = ["bump-my-version", "bump", part]
    
    if dry_run:
        cmd.append("--dry-run")
    
    print(f"🔄 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
        
        if dry_run:
            print("📋 Dry run output:")
            print(result.stdout)
        else:
            print("✅ Version bumped successfully!")
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running bump-my-version: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def check_bump_my_version_installed() -> bool:
    """Check if bump-my-version is installed."""
    try:
        subprocess.run(
            ["bump-my-version", "--version"],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_bump_my_version() -> None:
    """Install bump-my-version if not already installed."""
    print("📦 Installing bump-my-version...")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "bump-my-version"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ bump-my-version installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing bump-my-version: {e}")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def show_current_version(project_root: Path) -> None:
    """Show the current version from pyproject.toml."""
    pyproject_file = project_root / "pyproject.toml"
    
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return
    
    try:
        result = subprocess.run(
            ["bump-my-version", "show", "current"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"📋 Current version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error getting current version: {e}")
        print(f"stderr: {e.stderr}")


def main() -> None:
    """Main function to update version."""
    if len(sys.argv) < 2:
        print("Usage: python update_version.py <part> [--dry-run]")
        print("")
        print("Parts:")
        print("  patch    - for bug fixes (0.2.0 -> 0.2.1)")
        print("  minor    - for new features (0.2.0 -> 0.3.0)")
        print("  major    - for breaking changes (1.0.0 -> 2.0.0)")
        print("  show     - show current version")
        print("")
        print("Options:")
        print("  --dry-run  - show what would be changed without making changes")
        print("")
        print("Examples:")
        print("  python update_version.py patch")
        print("  python update_version.py minor --dry-run")
        print("  python update_version.py show")
        sys.exit(1)
    
    part = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Check if bump-my-version is installed
    if not check_bump_my_version_installed():
        print("❌ bump-my-version is not installed")
        install_choice = input("Would you like to install it now? (y/n): ")
        if install_choice.lower() in ['y', 'yes']:
            install_bump_my_version()
        else:
            print("Please install bump-my-version manually:")
            print("  pip install bump-my-version")
            sys.exit(1)
    
    if part == "show":
        show_current_version(project_root)
        return
    
    # Validate part
    valid_parts = ["patch", "minor", "major"]
    if part not in valid_parts:
        print(f"❌ Invalid part: {part}")
        print(f"Valid parts: {', '.join(valid_parts)}")
        sys.exit(1)
    
    print(f"🔧 Updating version ({part}) for TestRail API Module")
    print(f"📁 Project root: {project_root}")
    
    # Run bump-my-version
    run_bump_version(project_root, part, dry_run)
    
    if not dry_run:
        print("\n🎉 Version update completed!")
        print("📋 Next steps:")
        print("   1. Review the changes")
        print("   2. Run tests to ensure everything works")
        print("   3. Commit the changes")
        print("   4. Generate documentation with new version")
        print("   5. Create a release tag")


if __name__ == "__main__":
    main() 