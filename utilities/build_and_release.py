#!/usr/bin/env python3
"""
Build and release script for testrail_api_module.

This script automates the build and release process:
1. Runs tests and type checking
2. Updates version in pyproject.toml (optional)
3. Updates CHANGELOG.md (optional)
4. Builds the package
5. Creates git tag
6. Optionally pushes tag to trigger GitHub Actions workflow
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import toml
except ImportError:
    print("Error: 'toml' package is required. Install with: uv pip install toml")
    sys.exit(1)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_current_version() -> str:
    """Get the current version from pyproject.toml."""
    project_root = get_project_root()
    pyproject_path = project_root / "pyproject.toml"
    
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        sys.exit(1)
    
    try:
        with open(pyproject_path, "r", encoding="utf-8") as f:
            data = toml.load(f)
        
        return data["project"]["version"]
    except (KeyError, toml.TomlDecodeError) as e:
        print(f"❌ Error reading version from pyproject.toml: {e}")
        sys.exit(1)


def update_version_in_pyproject(new_version: str, dry_run: bool = False) -> None:
    """Update version in pyproject.toml."""
    project_root = get_project_root()
    pyproject_path = project_root / "pyproject.toml"
    
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return
    
    with open(pyproject_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace version line - handle both quoted and unquoted versions
    pattern = r'(version\s*=\s*")[^"]+(")'
    new_content = re.sub(pattern, rf'\g<1>{new_version}\g<2>', content)
    
    # Verify the replacement worked
    if new_content == content:
        print("⚠️  Warning: Could not find version line in pyproject.toml")
        print("   Please update version manually")
        return
    
    if dry_run:
        print(f"[DRY RUN] Would update version in pyproject.toml to: {new_version}")
        return
    
    with open(pyproject_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Updated version in pyproject.toml to: {new_version}")


def update_changelog(new_version: str, dry_run: bool = False) -> None:
    """Move unreleased entries to a new version section in CHANGELOG.md."""
    project_root = get_project_root()
    changelog_path = project_root / "CHANGELOG.md"
    
    if not changelog_path.exists():
        print("⚠️  CHANGELOG.md not found, skipping changelog update")
        return
    
    with open(changelog_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if there's an [Unreleased] section
    if "## [Unreleased]" not in content:
        print("⚠️  No [Unreleased] section found in CHANGELOG.md")
        if not dry_run:
            response = input("Create new version section anyway? (y/N): ")
            if response.lower() != "y":
                return
        else:
            print("  [DRY RUN] Would create new version section")
            return
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Replace [Unreleased] with new version section
    new_section = f"## [{new_version}] {today}"
    new_content = content.replace("## [Unreleased]", new_section, 1)
    
    # Add new [Unreleased] section after the version section
    # Find the end of the new version section (next ## or end of file)
    lines = new_content.split("\n")
    insert_index = None
    
    for i, line in enumerate(lines):
        if line.startswith(f"## [{new_version}]"):
            # Find the next ## or end of file
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("## "):
                    insert_index = j
                    break
            if insert_index is None:
                insert_index = len(lines)
            break
    
    if insert_index is not None:
        lines.insert(insert_index, "")
        lines.insert(insert_index + 1, "## [Unreleased]")
        lines.insert(insert_index + 2, "")
        new_content = "\n".join(lines)
    
    if dry_run:
        print(f"[DRY RUN] Would update CHANGELOG.md:")
        print(f"  - Move [Unreleased] entries to [{new_version}] {today}")
        print(f"  - Add new [Unreleased] section")
        return
    
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ Updated CHANGELOG.md with version {new_version}")


def run_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    check: bool = True,
    dry_run: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    """Run a shell command."""
    if dry_run:
        print(f"[DRY RUN] Would run: {' '.join(cmd)}")
        return subprocess.CompletedProcess(cmd, 0, b"", b"")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd or get_project_root(),
        check=check,
        capture_output=False,
    )
    return result


def run_tests(dry_run: bool = False) -> bool:
    """Run the test suite."""
    print("\n🧪 Running tests...")
    try:
        run_command(
            [sys.executable, "-m", "pytest", "-v"],
            dry_run=dry_run,
        )
        print("✅ Tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        return False


def run_type_check(dry_run: bool = False) -> bool:
    """Run mypy type checking."""
    print("\n🔍 Running type checks...")
    try:
        run_command(
            [sys.executable, "-m", "mypy", "src/testrail_api_module"],
            dry_run=dry_run,
        )
        print("✅ Type checks passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Type checks failed")
        return False


def build_package(dry_run: bool = False) -> bool:
    """Build the package."""
    print("\n📦 Building package...")
    try:
        run_command(
            [sys.executable, "-m", "build"],
            dry_run=dry_run,
        )
        print("✅ Package built successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Package build failed")
        return False


def check_tag_exists(version: str) -> bool:
    """Check if a git tag already exists."""
    tag_name = f"v{version}" if not version.startswith("v") else version
    try:
        result = subprocess.run(
            ["git", "tag", "-l", tag_name],
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_git_tag(version: str, message: Optional[str] = None, dry_run: bool = False) -> bool:
    """Create a git tag for the release."""
    if not is_git_repo():
        print("⚠️  Not in a git repository, skipping tag creation")
        return True  # Not an error, just skip
    
    tag_name = f"v{version}" if not version.startswith("v") else version
    
    # Check if tag already exists
    if not dry_run and check_tag_exists(version):
        print(f"⚠️  Tag {tag_name} already exists")
        response = input(f"Delete and recreate tag {tag_name}? (y/N): ")
        if response.lower() == "y":
            try:
                subprocess.run(
                    ["git", "tag", "-d", tag_name],
                    check=True,
                    capture_output=True,
                )
                print(f"✅ Deleted existing tag: {tag_name}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to delete existing tag: {tag_name}")
                return False
        else:
            print(f"⚠️  Skipping tag creation (tag already exists)")
            return True
    
    if message is None:
        message = f"Release {tag_name}"
    
    print(f"\n🏷️  Creating git tag: {tag_name}")
    
    try:
        run_command(
            ["git", "tag", "-a", tag_name, "-m", message],
            dry_run=dry_run,
        )
        if not dry_run:
            print(f"✅ Created tag: {tag_name}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to create tag: {tag_name}")
        return False


def push_tag(version: str, dry_run: bool = False) -> bool:
    """Push the git tag to remote."""
    if not is_git_repo():
        print("⚠️  Not in a git repository, skipping tag push")
        return True  # Not an error, just skip
    
    tag_name = f"v{version}" if not version.startswith("v") else version
    
    print(f"\n📤 Pushing tag to remote: {tag_name}")
    
    try:
        run_command(
            ["git", "push", "origin", tag_name],
            dry_run=dry_run,
        )
        if not dry_run:
            print(f"✅ Pushed tag: {tag_name}")
            print("🚀 GitHub Actions workflow should trigger automatically")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to push tag: {tag_name}")
        print("   Make sure you have push access and the remote is configured")
        return False


def is_git_repo() -> bool:
    """Check if we're in a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_git_status() -> bool:
    """Check if there are uncommitted changes."""
    if not is_git_repo():
        print("⚠️  Warning: Not in a git repository")
        return True  # Continue anyway, might be building only
    
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        
        if result.stdout.strip():
            print("⚠️  Warning: You have uncommitted changes:")
            print(result.stdout)
            return False
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Warning: Could not check git status (git may not be available)")
        return True  # Continue anyway


def validate_version(version: str) -> bool:
    """Validate version format (semantic versioning)."""
    # Remove 'v' prefix if present for validation
    version_clean = version.lstrip("v")
    
    # Basic semver pattern: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
    pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$"
    
    if not re.match(pattern, version_clean):
        print(f"❌ Invalid version format: {version}")
        print("   Expected format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]")
        print("   Examples: 0.5.2, 1.0.0, 1.0.0-alpha.1, 1.0.0-beta.1+20240101")
        return False
    
    return True


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build and release script for testrail_api_module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run to see what would happen
  python utilities/build_and_release.py --version 0.5.3 --dry-run

  # Build and create tag (without pushing)
  python utilities/build_and_release.py --version 0.5.3 --skip-push

  # Full release (build, tag, and push)
  python utilities/build_and_release.py --version 0.5.3

  # Skip tests and type checks (not recommended)
  python utilities/build_and_release.py --version 0.5.3 --skip-tests --skip-type-check

  # Only build package without version updates
  python utilities/build_and_release.py --build-only
        """,
    )
    
    parser.add_argument(
        "--version",
        type=str,
        help="New version number (e.g., 0.5.3 or v0.5.3)",
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )
    
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests",
    )
    
    parser.add_argument(
        "--skip-type-check",
        action="store_true",
        help="Skip type checking",
    )
    
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip building the package",
    )
    
    parser.add_argument(
        "--skip-push",
        action="store_true",
        help="Create tag but don't push to remote",
    )
    
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Only build the package (skip version updates, changelog, and tagging)",
    )
    
    parser.add_argument(
        "--tag-message",
        type=str,
        help="Custom message for the git tag",
    )
    
    parser.add_argument(
        "--skip-changelog",
        action="store_true",
        help="Skip updating CHANGELOG.md",
    )
    
    args = parser.parse_args()
    
    project_root = get_project_root()
    os.chdir(project_root)
    
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    if args.build_only:
        # Just build the package
        if not args.skip_build:
            if not build_package(dry_run=args.dry_run):
                sys.exit(1)
        print("\n✅ Build complete")
        return
    
    # Validate version if provided
    if args.version:
        if not validate_version(args.version):
            sys.exit(1)
        
        # Normalize version (remove 'v' prefix for internal use)
        new_version = args.version.lstrip("v")
        
        if new_version == current_version:
            print(f"⚠️  Version {new_version} is already the current version")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != "y":
                sys.exit(0)
    else:
        print("❌ --version is required (unless using --build-only)")
        print(f"\n💡 Tip: Current version is {current_version}")
        print("   To do a dry run, use: --version <new_version> --dry-run")
        print("   To just build, use: --build-only")
        parser.print_help()
        sys.exit(1)
    
    # Check git status
    if not args.dry_run and not check_git_status():
        response = input("\nContinue with uncommitted changes? (y/N): ")
        if response.lower() != "y":
            sys.exit(0)
    
    # Run tests
    if not args.skip_tests:
        if not run_tests(dry_run=args.dry_run):
            if not args.dry_run:
                sys.exit(1)
    
    # Run type checks
    if not args.skip_type_check:
        if not run_type_check(dry_run=args.dry_run):
            if not args.dry_run:
                sys.exit(1)
    
    # Update version
    if args.version:
        update_version_in_pyproject(new_version, dry_run=args.dry_run)
    
    # Update changelog
    if args.version and not args.skip_changelog:
        update_changelog(new_version, dry_run=args.dry_run)
    
    # Build package
    if not args.skip_build:
        if not build_package(dry_run=args.dry_run):
            if not args.dry_run:
                sys.exit(1)
    
    # Create git tag
    if args.version:
        if not create_git_tag(new_version, args.tag_message, dry_run=args.dry_run):
            if not args.dry_run:
                sys.exit(1)
    
    # Push tag
    if args.version and not args.skip_push:
        if not args.dry_run:
            response = input(f"\nPush tag v{new_version} to trigger GitHub Actions? (y/N): ")
            if response.lower() == "y":
                if not push_tag(new_version, dry_run=args.dry_run):
                    sys.exit(1)
            else:
                print(f"\n⚠️  Tag v{new_version} created locally but not pushed")
                print(f"   Push manually with: git push origin v{new_version}")
        else:
            push_tag(new_version, dry_run=args.dry_run)
    
    print("\n✅ Release process complete!")
    
    if args.dry_run:
        print("\n[DRY RUN] No changes were made. Run without --dry-run to execute.")
    elif args.version and args.skip_push:
        print(f"\n📌 Next steps:")
        print(f"   1. Review changes: git diff")
        print(f"   2. Commit changes: git add pyproject.toml CHANGELOG.md")
        print(f"   3. Push tag: git push origin v{new_version}")


if __name__ == "__main__":
    main()
