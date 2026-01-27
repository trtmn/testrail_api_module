#!/usr/bin/env python3
"""
Build and release script for testrail_api_module.

This script automates the build and release process:
1. Runs tests and type checking
2. Updates version in pyproject.toml
3. Updates CHANGELOG.md
4. Builds the package
5. Creates a PR to merge the changes into the release branch

Optionally, use --tag to create and push a git tag (only works on release branch).
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_current_version() -> str:
    """Get the current version using uv."""
    project_root = get_project_root()
    
    try:
        result = subprocess.run(
            ["uv", "version", "--short"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error reading version with uv: {e}")
        print("   Make sure uv is installed and available in PATH")
        sys.exit(1)


def bump_version(
    bump_type: str,
    dry_run: bool = False,
) -> str:
    """Bump the version using uv version --bump.
    
    Args:
        bump_type: Type of bump (major, minor, patch, stable, alpha, beta, rc, post, dev)
        dry_run: If True, don't actually update the version
    
    Returns:
        The new version string
    """
    project_root = get_project_root()
    
    cmd = ["uv", "version", "--bump", bump_type]
    if dry_run:
        cmd.append("--dry-run")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        
        # uv version --bump outputs: "package-name 0.5.2 => 0.5.3"
        # Extract the new version (after "=>")
        output = result.stdout.strip()
        if "=>" in output:
            # Extract version after "=>"
            new_version = output.split("=>")[-1].strip()
        else:
            # Fallback: try to extract version from output
            new_version = output
        
        if dry_run:
            print(f"[DRY RUN] Would bump version to: {new_version}")
        else:
            print(f"✅ Bumped version to: {new_version}")
        
        return new_version
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error bumping version with uv: {e}")
        print("   Make sure uv is installed and available in PATH")
        sys.exit(1)


def update_version_in_pyproject(new_version: str, dry_run: bool = False) -> None:
    """Update version in pyproject.toml using uv."""
    project_root = get_project_root()
    
    cmd = ["uv", "version", new_version]
    if dry_run:
        cmd.append("--dry-run")
        print(f"[DRY RUN] Would update version to: {new_version}")
        try:
            subprocess.run(
                cmd,
                cwd=project_root,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"⚠️  Warning: Could not run uv version: {e}")
        return
    
    try:
        subprocess.run(
            cmd,
            cwd=project_root,
            check=True,
            capture_output=True,
        )
        print(f"✅ Updated version in pyproject.toml to: {new_version}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ Error updating version with uv: {e}")
        print("   Make sure uv is installed and available in PATH")
        sys.exit(1)


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
    """Run the test suite.
    
    Note: Tests always run, even in dry-run mode, since they don't modify anything.
    """
    if dry_run:
        print("\n🧪 Running tests (dry-run mode - tests still execute)...")
    else:
        print("\n🧪 Running tests...")
    
    try:
        # Always run tests, even in dry-run mode (they don't modify anything)
        run_command(
            [sys.executable, "-m", "pytest", "-v"],
            dry_run=False,  # Force actual execution
        )
        print("✅ Tests passed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        return False


def run_type_check(dry_run: bool = False) -> bool:
    """Run mypy type checking.
    
    Note: Type checks always run, even in dry-run mode, since they don't modify anything.
    """
    if dry_run:
        print("\n🔍 Running type checks (dry-run mode - checks still execute)...")
    else:
        print("\n🔍 Running type checks...")
    
    try:
        # Always run type checks, even in dry-run mode (they don't modify anything)
        run_command(
            [sys.executable, "-m", "mypy", "src/testrail_api_module"],
            dry_run=False,  # Force actual execution
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


def get_current_branch() -> Optional[str]:
    """Get the current git branch name."""
    if not is_git_repo():
        return None
    
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_remote_repo_info() -> Optional[tuple[str, str]]:
    """Get the GitHub repository owner and name from remote URL.
    
    Returns:
        Tuple of (owner, repo) or None if not available
    """
    if not is_git_repo():
        return None
    
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        remote_url = result.stdout.strip()
        
        # Handle both SSH and HTTPS URLs
        # SSH: git@github.com:owner/repo.git
        # HTTPS: https://github.com/owner/repo.git
        patterns = [
            r"git@github\.com:(.+?)/(.+?)(?:\.git)?$",
            r"https?://github\.com/(.+?)/(.+?)(?:\.git)?$",
        ]
        
        for pattern in patterns:
            match = re.match(pattern, remote_url)
            if match:
                return (match.group(1), match.group(2))
        
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def commit_release_changes(version: str, dry_run: bool = False) -> bool:
    """Commit version and changelog changes."""
    if not is_git_repo():
        print("⚠️  Not in a git repository, skipping commit")
        return True  # Not an error, just skip
    
    project_root = get_project_root()
    
    # Check if there are changes to commit
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", "pyproject.toml", "CHANGELOG.md"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        
        if not result.stdout.strip():
            print("ℹ️  No changes to commit (files may already be committed)")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Could not check git status")
        return False
    
    if dry_run:
        print("[DRY RUN] Would commit changes:")
        print("  - git add pyproject.toml CHANGELOG.md")
        print(f"  - git commit -m 'Prepare release v{version}'")
        return True
    
    try:
        # Stage the files
        subprocess.run(
            ["git", "add", "pyproject.toml", "CHANGELOG.md"],
            cwd=project_root,
            check=True,
            capture_output=True,
        )
        
        # Commit
        commit_message = f"Prepare release v{version}"
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=project_root,
            check=True,
            capture_output=True,
        )
        
        print(f"✅ Committed changes for release v{version}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to commit changes: {e}")
        return False


def push_branch(branch_name: str, dry_run: bool = False) -> bool:
    """Push the current branch to remote."""
    if not is_git_repo():
        print("⚠️  Not in a git repository, skipping push")
        return True  # Not an error, just skip
    
    project_root = get_project_root()
    
    if dry_run:
        print(f"[DRY RUN] Would push branch {branch_name} to origin")
        return True
    
    try:
        # Check if branch exists on remote
        result = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch_name],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        
        branch_exists_remote = bool(result.stdout.strip())
        
        if branch_exists_remote:
            # Branch exists, push updates
            subprocess.run(
                ["git", "push", "origin", branch_name],
                cwd=project_root,
                check=True,
            )
        else:
            # New branch, set upstream
            subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                cwd=project_root,
                check=True,
            )
        
        print(f"✅ Pushed branch {branch_name} to origin")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to push branch {branch_name}: {e}")
        print("   Make sure you have push access and the remote is configured")
        return False


def create_release_pr(
    version: str,
    release_branch: str = "release",
    dry_run: bool = False,
) -> Optional[str]:
    """Create a pull request to merge changes into the release branch.
    
    Args:
        version: The release version
        release_branch: The target branch for the PR (default: "release")
        dry_run: If True, don't actually create the PR
    
    Returns:
        PR URL if created successfully, None otherwise
    """
    if not is_git_repo():
        print("⚠️  Not in a git repository, skipping PR creation")
        return None
    
    # Get current branch
    current_branch = get_current_branch()
    if not current_branch:
        print("⚠️  Could not determine current branch, skipping PR creation")
        return None
    
    # Get repository info
    repo_info = get_remote_repo_info()
    if not repo_info:
        print("⚠️  Could not determine repository info, skipping PR creation")
        print("   Make sure 'origin' remote is configured correctly")
        return None
    
    owner, repo = repo_info
    
    if dry_run:
        print(f"[DRY RUN] Would create PR:")
        print(f"  - From: {current_branch}")
        print(f"  - To: {release_branch}")
        print(f"  - Title: Prepare release v{version}")
        return None
    
    # Create PR using GitHub MCP
    try:
        # Import here to avoid dependency if MCP is not available
        # We'll use subprocess to call the MCP tool via a helper or direct API
        # For now, we'll provide instructions and use gh CLI if available
        # Otherwise, we'll print the URL to create manually
        
        # Try using gh CLI first
        try:
            pr_body = f"""## Release v{version}

This PR prepares the release of version {version}.

### Changes
- Updated version in `pyproject.toml` to {version}
- Updated `CHANGELOG.md` with release notes

### Next Steps
After this PR is merged, the release tag will be created.
"""
            
            result = subprocess.run(
                [
                    "gh", "pr", "create",
                    "--base", release_branch,
                    "--head", current_branch,
                    "--title", f"Prepare release v{version}",
                    "--body", pr_body,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            
            pr_url = result.stdout.strip()
            print(f"✅ Created pull request: {pr_url}")
            return pr_url
        except (subprocess.CalledProcessError, FileNotFoundError):
            # gh CLI not available, provide manual instructions
            print("⚠️  GitHub CLI (gh) not available")
            print(f"\n📝 To create the PR manually:")
            print(f"   1. Go to: https://github.com/{owner}/{repo}/compare/{release_branch}...{current_branch}")
            print(f"   2. Title: Prepare release v{version}")
            print(f"   3. Description: Release preparation for version {version}")
            print(f"   4. Click 'Create pull request'")
            return None
    except Exception as e:
        print(f"❌ Failed to create PR: {e}")
        return None


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


def confirm_step(prompt: str, default: bool = False, non_interactive: bool = False) -> bool:
    """Prompt user to confirm a step.
    
    Args:
        prompt: The prompt message to display
        default: Default value if user just presses Enter (True = yes, False = no)
        non_interactive: If True, skip prompt and return default value
    
    Returns:
        True if user confirms, False otherwise
    """
    if non_interactive:
        return default
    
    default_text = "Y/n" if default else "y/N"
    response = input(f"{prompt} ({default_text}): ").strip().lower()
    
    if not response:
        return default
    
    return response in ("y", "yes")


def prompt_version_bump(
    current_version: str,
    non_interactive: bool = False,
) -> Optional[str]:
    """Prompt user to select a version bump type.
    
    Args:
        current_version: The current version string
        non_interactive: If True, skip prompt and return None
    
    Returns:
        Bump type (major, minor, patch, etc.) or None if cancelled
    """
    if non_interactive:
        return None
    
    print(f"\n📋 Current version: {current_version}")
    print("\nSelect version bump type:")
    print("  1. patch  - Bug fixes (0.5.2 → 0.5.3)")
    print("  2. minor  - New features (0.5.2 → 0.6.0)")
    print("  3. major  - Breaking changes (0.5.2 → 1.0.0)")
    print("  4. alpha  - Alpha pre-release")
    print("  5. beta   - Beta pre-release")
    print("  6. rc     - Release candidate")
    print("  7. stable - Remove pre-release suffix")
    print("  8. post   - Post-release")
    print("  9. dev    - Development version")
    print("  0. Cancel")
    
    bump_map = {
        "1": "patch",
        "2": "minor",
        "3": "major",
        "4": "alpha",
        "5": "beta",
        "6": "rc",
        "7": "stable",
        "8": "post",
        "9": "dev",
    }
    
    while True:
        choice = input("\nEnter your choice (1-9, or 0 to cancel): ").strip()
        
        if choice == "0":
            return None
        
        if choice in bump_map:
            return bump_map[choice]
        
        print("❌ Invalid choice. Please enter 1-9 or 0 to cancel.")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build and release script for testrail_api_module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (default) - prompts for version bump type and confirmation at each step
  python utilities/build_and_release.py

  # Specify version explicitly
  python utilities/build_and_release.py --version 0.5.3

  # Dry run to see what would happen
  python utilities/build_and_release.py --dry-run

  # Non-interactive mode (for automation/CI) - requires --version
  python utilities/build_and_release.py --version 0.5.3 --non-interactive

  # Create PR to different release branch
  python utilities/build_and_release.py --version 0.5.3 --release-branch main

  # Skip PR creation
  python utilities/build_and_release.py --version 0.5.3 --skip-pr

  # Create and push tag (must be on release branch, uses version from pyproject.toml)
  python utilities/build_and_release.py --tag

  # Create and push tag with specific version
  python utilities/build_and_release.py --version 0.5.3 --tag

  # Skip tests and type checks (not recommended)
  python utilities/build_and_release.py --version 0.5.3 --skip-tests --skip-type-check

  # Only build package without version updates
  python utilities/build_and_release.py --build-only
        """,
    )
    
    parser.add_argument(
        "--version",
        type=str,
        help="New version number (e.g., 0.5.3 or v0.5.3). If not provided, will prompt for bump type (major/minor/patch).",
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
    
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Skip all interactive prompts (useful for automation)",
    )
    
    parser.add_argument(
        "--release-branch",
        type=str,
        default="release",
        help="Target branch for the release PR (default: release)",
    )
    
    parser.add_argument(
        "--skip-pr",
        action="store_true",
        help="Skip creating a pull request",
    )
    
    parser.add_argument(
        "--tag",
        action="store_true",
        help="Create and push a git tag using current version from pyproject.toml (only works on release branch)",
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
    
    # Handle version: required unless using --tag-only or --build-only
    # If --tag is used without --version, use current version from pyproject.toml
    tag_only_mode = args.tag and not args.version
    if tag_only_mode:
        # For tag-only operation, use current version and skip release steps
        new_version = current_version
        print(f"Using current version from pyproject.toml: {new_version}")
        print("Tag-only mode: skipping release steps (tests, version update, changelog, build, PR)")
    elif args.version:
        if not validate_version(args.version):
            sys.exit(1)
        
        # Normalize version (remove 'v' prefix for internal use)
        new_version = args.version.lstrip("v")
        
        if new_version == current_version:
            print(f"⚠️  Version {new_version} is already the current version")
            response = input("Continue anyway? (y/N): ")
            if response.lower() != "y":
                sys.exit(0)
    elif not args.build_only:
        # No version specified - prompt for bump type
        # Note: dry-run should still allow interactive prompts, only --non-interactive skips them
        bump_type = prompt_version_bump(
            current_version,
            non_interactive=args.non_interactive,
        )
        
        if bump_type is None:
            if args.non_interactive:
                print("❌ Version bump cancelled (non-interactive mode requires --version)")
                sys.exit(1)
            else:
                print("❌ Version bump cancelled")
                sys.exit(0)
        
        # Show what the new version would be (dry run)
        if args.dry_run:
            print(f"\n[DRY RUN] Would bump version using: {bump_type}")
            # Get the new version from a dry run
            new_version = bump_version(bump_type, dry_run=True)
        else:
            # Actually bump the version
            new_version = bump_version(bump_type, dry_run=False)
        
        print(f"New version: {new_version}")
    
    # Skip release steps if tag-only mode
    if not tag_only_mode:
        # Check git status
        if not args.dry_run and not check_git_status():
            response = input("\nContinue with uncommitted changes? (y/N): ")
            if response.lower() != "y":
                sys.exit(0)
        
        # Run tests
        if not args.skip_tests:
            if not confirm_step(
                "\n🧪 Proceed with running tests?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping tests (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                if not run_tests(dry_run=args.dry_run):
                    # Always exit on test failure, even in dry-run mode
                    print("❌ Tests failed - fix issues before proceeding")
                    sys.exit(1)
        
        # Run type checks
        if not args.skip_type_check:
            if not confirm_step(
                "\n🔍 Proceed with type checking?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping type checks (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                if not run_type_check(dry_run=args.dry_run):
                    # Always exit on type check failure, even in dry-run mode
                    print("❌ Type checks failed - fix issues before proceeding")
                    sys.exit(1)
        
        # Update version (if version was explicitly provided, not if it was bumped)
        # When version is bumped, it's already updated, so we skip this step
        if args.version and new_version != current_version:
            if not confirm_step(
                f"\n📝 Update version from {current_version} to {new_version}?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping version update (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                update_version_in_pyproject(new_version, dry_run=args.dry_run)
        
        # Update changelog (always update if we have a new version)
        if new_version != current_version and not args.skip_changelog:
            if not confirm_step(
                f"\n📄 Update CHANGELOG.md for version {new_version}?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping changelog update (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                update_changelog(new_version, dry_run=args.dry_run)
        
        # Build package
        if not args.skip_build:
            if not confirm_step(
                "\n📦 Proceed with building the package?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping package build (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                if not build_package(dry_run=args.dry_run):
                    if not args.dry_run:
                        sys.exit(1)
        
        # Commit and create PR (always create if we have a new version)
        if new_version != current_version and not args.skip_pr:
            # Commit the changes first
            if not confirm_step(
                f"\n💾 Commit version and changelog changes for v{new_version}?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping commit (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                if not commit_release_changes(new_version, dry_run=args.dry_run):
                    if not args.dry_run:
                        sys.exit(1)
                
                # Push the branch
                current_branch = get_current_branch()
                if current_branch:
                    if not confirm_step(
                        f"\n📤 Push branch '{current_branch}' to remote?",
                        default=True,
                        non_interactive=args.non_interactive or args.dry_run,
                    ):
                        print("⚠️  Skipping branch push (user cancelled)")
                        if not args.non_interactive:
                            sys.exit(0)
                    else:
                        if not push_branch(current_branch, dry_run=args.dry_run):
                            if not args.dry_run:
                                sys.exit(1)
                
                # Create PR
                if not confirm_step(
                    f"\n🔀 Create pull request to merge into '{args.release_branch}' branch?",
                    default=True,
                    non_interactive=args.non_interactive or args.dry_run,
                ):
                    print("⚠️  Skipping PR creation (user cancelled)")
                    if not args.non_interactive:
                        sys.exit(0)
                else:
                    pr_url = create_release_pr(
                        new_version,
                        release_branch=args.release_branch,
                        dry_run=args.dry_run,
                    )
                    if pr_url and not args.dry_run:
                        print(f"\n📌 PR created: {pr_url}")
                        print("   Wait for the PR to be reviewed and merged before creating the tag.")
    
    # Handle tag creation (only with --tag flag, and only on release branch)
    if args.tag:
        current_branch = get_current_branch()
        if not current_branch:
            print("❌ Could not determine current branch")
            sys.exit(1)
        
        if current_branch != args.release_branch:
            print(f"❌ Tag creation is only allowed on the release branch ({args.release_branch})")
            print(f"   Current branch: {current_branch}")
            print(f"   Please checkout the release branch first:")
            print(f"   git checkout {args.release_branch}")
            sys.exit(1)
        
        tag_name = f"v{new_version}"
        
        # Create tag
        if not confirm_step(
            f"\n🏷️  Create git tag {tag_name} on {args.release_branch} branch?",
            default=True,
            non_interactive=args.non_interactive or args.dry_run,
        ):
            print("⚠️  Skipping tag creation (user cancelled)")
            if not args.non_interactive:
                sys.exit(0)
        else:
            if not create_git_tag(new_version, args.tag_message, dry_run=args.dry_run):
                if not args.dry_run:
                    sys.exit(1)
            
            # Auto-push tag after creation
            if not confirm_step(
                f"\n📤 Push tag {tag_name} to remote to trigger GitHub Actions?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print(f"\n⚠️  Tag {tag_name} created locally but not pushed")
                print(f"   Push manually with: git push origin {tag_name}")
            else:
                if not push_tag(new_version, dry_run=args.dry_run):
                    sys.exit(1)
    
    print("\n✅ Release process complete!")
    
    if args.dry_run:
        print("\n[DRY RUN] No changes were made. Run without --dry-run to execute.")
    elif args.version:
        if not args.skip_pr:
            print(f"\n📌 Next steps:")
            print(f"   1. Review and merge the pull request")
            if not args.tag:
                print(f"   2. After PR is merged, checkout release branch and create tag:")
                print(f"      git checkout {args.release_branch}")
                print(f"      python utilities/build_and_release.py --tag")
        else:
            if not args.tag:
                print(f"\n💡 To create and push a tag, use:")
                print(f"   python utilities/build_and_release.py --tag")
                print(f"   (Must be on {args.release_branch} branch, uses version from pyproject.toml)")


if __name__ == "__main__":
    main()
