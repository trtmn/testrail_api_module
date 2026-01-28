#!/usr/bin/env python3
"""
Build and release script for testrail_api_module using GitFlow workflow.

GitFlow Workflow:
1. dev branch → main: Version bump happens here, then merge to main (main is protected)
2. main → release: Merge main into release branch (version already set)
3. release branch: Where version tags are created and pushed

Branch-specific behavior:
- On dev branch: Bumps version, updates changelog, creates PR to merge into main
- On main branch: Prepares release (no version bump, version already set), creates PR to release branch
- On release branch: Creates and pushes version tags (use --tag flag)

This script automates:
1. Running tests and type checking
2. Updating version in pyproject.toml (dev→main only, since main is protected)
3. Updating CHANGELOG.md (dev→main only)
4. Building the package
5. Creating appropriate PRs based on current branch (fully created, not drafts)
6. Creating and pushing git tags (release branch only)
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


def update_version_in_pyproject(
        new_version: str,
        dry_run: bool = False) -> None:
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
        print("[DRY RUN] Would update CHANGELOG.md:")
        print(f"  - Move [Unreleased] entries to [{new_version}] {today}")
        print("  - Add new [Unreleased] section")
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
        # Always run type checks, even in dry-run mode (they don't modify
        # anything)
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
    """Build the package using uv."""
    print("\n📦 Building package...")
    try:
        run_command(
            ["uv", "build"],
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


def create_git_tag(
        version: str,
        message: Optional[str] = None,
        dry_run: bool = False) -> bool:
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
            print("⚠️  Skipping tag creation (tag already exists)")
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
    """Commit version and changelog changes.
    
    This function commits both pyproject.toml and CHANGELOG.md changes.
    It will include any existing uncommitted changes to these files, ensuring
    the changelog is up-to-date on the release branch.
    """
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
        
        changes = result.stdout.strip()
        if not changes:
            print("ℹ️  No changes to commit (files may already be committed)")
            return True
        
        # Show what will be committed
        if changes:
            print("📝 Changes to be committed:")
            for line in changes.split("\n"):
                if line.strip():
                    status, file = line.split(maxsplit=1)
                    print(f"   {status} {file}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Could not check git status")
        return False

    if dry_run:
        print("[DRY RUN] Would commit changes:")
        print("  - git add pyproject.toml CHANGELOG.md")
        print(f"  - git commit -m 'Prepare release v{version}'")
        return True

    try:
        # Stage the files (this will include any existing uncommitted changes)
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
        print("   (Includes version update and changelog changes)")
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
    workflow_type: str = "main_to_release",
    dry_run: bool = False,
) -> Optional[str]:
    """Create a pull request using GitHub API (via MCP or gh CLI).
    
    Args:
        version: The release version (or current version for dev→main)
        release_branch: The target branch for the PR
        workflow_type: The workflow type (dev_to_main or main_to_release)
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
    
    # Determine PR title and body based on workflow
    if workflow_type == "dev_to_main":
        pr_title = f"Merge dev to main (v{version})"
        pr_body = f"""## Merge dev to main

This PR merges development changes into the main branch.

### Changes
- Version bumped to {version}
- Updated `pyproject.toml` with new version
- Updated `CHANGELOG.md` with release notes

### Next Steps
After this PR is merged to main, create a PR from main to release branch.
"""
    else:  # main_to_release
        pr_title = f"Prepare release v{version}"
        pr_body = f"""## Release v{version}

This PR prepares the release of version {version} by merging main into the release branch.

### Changes
- Version: {version}
- Ready for release tagging

### Next Steps
After this PR is merged to release branch, use `--tag` flag to create and push the version tag.
"""
    
    if dry_run:
        print("[DRY RUN] Would create PR:")
        print(f"  - From: {current_branch}")
        print(f"  - To: {release_branch}")
        print(f"  - Title: {pr_title}")
        return None
    
    # Try using gh CLI (creates full PR, not draft by default)
    try:
        result = subprocess.run(
            [
                "gh", "pr", "create",
                "--base", release_branch,
                "--head", current_branch,
                "--title", pr_title,
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
        # gh CLI not available - provide manual instructions
        print("⚠️  GitHub CLI (gh) not available")
        print(f"\n📝 To create the PR manually (make sure to create it fully, NOT as draft):")
        print(f"   1. Go to: https://github.com/{owner}/{repo}/compare/{release_branch}...{current_branch}")
        print(f"   2. Title: {pr_title}")
        print(f"   3. Description: {pr_body}")
        print(f"   4. Click 'Create pull request' (NOT 'Create draft pull request')")
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


def is_protected_branch(branch_name: Optional[str] = None) -> bool:
    """Check if the current branch (or specified branch) is protected.
    
    Protected branches are typically main, master, or release branches
    where direct commits are not allowed.
    
    Args:
        branch_name: Branch name to check. If None, checks current branch.
    
    Returns:
        True if the branch is protected, False otherwise
    """
    if branch_name is None:
        branch_name = get_current_branch()
    
    if not branch_name:
        return False
    
    # Common protected branch names
    protected_branches = {"main", "master", "release"}
    return branch_name in protected_branches


def get_gitflow_context() -> tuple[str, Optional[str]]:
    """Determine the GitFlow workflow context based on current branch.
    
    Returns:
        Tuple of (workflow_type, target_branch) where:
        - workflow_type: "dev_to_main", "main_to_release", "release_tag", or "unknown"
        - target_branch: The target branch for PRs (None for release_tag)
    """
    current_branch = get_current_branch()
    
    if not current_branch:
        return ("unknown", None)
    
    # GitFlow branch detection
    if current_branch == "dev" or current_branch.startswith("dev/"):
        return ("dev_to_main", "main")
    elif current_branch == "main" or current_branch == "master":
        return ("main_to_release", "release")
    elif current_branch == "release" or current_branch.startswith("release/"):
        return ("release_tag", None)
    else:
        # Default: assume feature branch that should go to main
        return ("dev_to_main", "main")


def create_and_checkout_branch(branch_name: str, dry_run: bool = False) -> bool:
    """Create and checkout a new branch.
    
    Args:
        branch_name: Name of the branch to create
        dry_run: If True, don't actually create the branch
    
    Returns:
        True if successful, False otherwise
    """
    if not is_git_repo():
        print("⚠️  Not in a git repository, cannot create branch")
        return False
    
    project_root = get_project_root()
    
    # Check if branch already exists
    try:
        result = subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
            cwd=project_root,
            capture_output=True,
        )
        branch_exists = result.returncode == 0
        
        if branch_exists:
            print(f"⚠️  Branch '{branch_name}' already exists")
            response = input(f"Checkout existing branch '{branch_name}'? (y/N): ")
            if response.lower() != "y":
                return False
        else:
            if dry_run:
                print(f"[DRY RUN] Would create and checkout branch: {branch_name}")
                return True
            
            # Create new branch
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=project_root,
                check=True,
                capture_output=True,
            )
            print(f"✅ Created and checked out branch: {branch_name}")
            return True
        
        # Branch exists, just checkout
        if not dry_run:
            subprocess.run(
                ["git", "checkout", branch_name],
                cwd=project_root,
                check=True,
                capture_output=True,
            )
            print(f"✅ Checked out branch: {branch_name}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create/checkout branch '{branch_name}': {e}")
        return False


def check_and_commit_version_changes(version: str, workflow_type: str, dry_run: bool = False) -> bool:
    """Check for uncommitted changes and commit if they're only version-related files.
    
    Args:
        version: The version string (for commit message)
        workflow_type: The workflow type (dev_to_main, main_to_release, etc.)
        dry_run: If True, don't actually commit
    
    Returns:
        True if we can proceed (no changes or changes committed), False otherwise
    """
    if not is_git_repo():
        print("⚠️  Warning: Not in a git repository")
        return True  # Continue anyway, might be building only
    
    project_root = get_project_root()
    
    try:
        # Check all uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        
        if not result.stdout.strip():
            return True  # No uncommitted changes
        
        # Version-related files that can be auto-committed
        version_files = ["pyproject.toml", "CHANGELOG.md", "uv.lock"]
        
        # Check if only version-related files are changed
        version_files_result = subprocess.run(
            ["git", "status", "--porcelain"] + version_files,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
        )
        
        # Get all changed files
        all_changes = result.stdout.strip().split("\n")
        version_changes = version_files_result.stdout.strip().split("\n") if version_files_result.stdout.strip() else []
        
        # Filter out empty strings
        all_changes = [c for c in all_changes if c.strip()]
        version_changes = [c for c in version_changes if c.strip()]
        
        # Extract just the filenames from git status output (format: " M filename" or "M  filename")
        all_changed_files = []
        for change in all_changes:
            parts = change.split()
            if len(parts) >= 2:
                # Get the filename (last part after status codes)
                filename = parts[-1]
                all_changed_files.append(filename)
        
        version_changed_files = []
        for change in version_changes:
            parts = change.split()
            if len(parts) >= 2:
                filename = parts[-1]
                version_changed_files.append(filename)
        
        # Check if only version files are changed (all changed files are in version files list)
        if len(all_changed_files) > 0 and all(filename in version_files for filename in all_changed_files):
            # Only version files are changed - auto-commit them
            changed_files_list = ", ".join(all_changed_files)
            print(f"📝 Found uncommitted version changes ({changed_files_list})")
            
            if workflow_type == "dev_to_main":
                commit_msg = f"Bump version to v{version}"
            else:
                commit_msg = f"Prepare release v{version}"
            
            if dry_run:
                print(f"[DRY RUN] Would commit version changes: {commit_msg}")
                return True
            
            # Commit the version changes
            try:
                # Add all version files that were changed
                files_to_add = [f for f in version_files if f in all_changed_files]
                subprocess.run(
                    ["git", "add"] + files_to_add,
                    cwd=project_root,
                    check=True,
                    capture_output=True,
                )
                subprocess.run(
                    ["git", "commit", "-m", commit_msg],
                    cwd=project_root,
                    check=True,
                    capture_output=True,
                )
                print(f"✅ Committed version changes: {commit_msg}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to commit version changes: {e}")
                return False
        else:
            # Other files are also changed - show warning
            print("⚠️  Warning: You have uncommitted changes:")
            print(result.stdout)
            return False
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Warning: Could not check git status (git may not be available)")
        return True  # Continue anyway


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


def confirm_step(prompt: str, default: bool = False,
                 non_interactive: bool = False) -> bool:
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
    """Main entry point for GitFlow-based build and release workflow."""
    parser = argparse.ArgumentParser(
        description="Build and release script for testrail_api_module (GitFlow workflow)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
GitFlow Workflow Examples:

  # On dev branch: Prepare PR to merge into main (no version bump)
  git checkout dev
  python utilities/build_and_release.py

  # On main branch: Prepare release, bump version, create PR to release branch
  git checkout main
  python utilities/build_and_release.py  # Will prompt for version bump type

  # On main branch: Prepare release with specific version
  git checkout main
  python utilities/build_and_release.py --version 0.5.3

  # On release branch: Create and push version tag
  git checkout release
  python utilities/build_and_release.py --tag

  # Dry run to see what would happen
  python utilities/build_and_release.py --dry-run

  # Non-interactive mode (for automation/CI) - requires --version
  python utilities/build_and_release.py --version 0.5.3 --non-interactive

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
    
    # Determine GitFlow context
    workflow_type, target_branch = get_gitflow_context()
    current_branch = get_current_branch()
    
    print(f"📍 Current branch: {current_branch}")
    print(f"🔄 Workflow: {workflow_type}")
    if target_branch:
        print(f"🎯 Target branch: {target_branch}")
    
    current_version = get_current_version()
    print(f"📦 Current version: {current_version}")
    
    if args.build_only:
        # Just build the package
        if not args.skip_build:
            if not build_package(dry_run=args.dry_run):
                sys.exit(1)
        print("\n✅ Build complete")
        return
    
    # Handle tag creation on release branch (separate workflow)
    if args.tag:
        if workflow_type != "release_tag":
            print(f"❌ Tag creation is only allowed on release branch")
            print(f"   Current branch: {current_branch}")
            print(f"   Please checkout the release branch first:")
            print(f"   git checkout release")
            sys.exit(1)
        
        # Use current version or specified version
        tag_version = current_version
        if args.version:
            if not validate_version(args.version):
                sys.exit(1)
            tag_version = args.version.lstrip("v")
        
        tag_name = f"v{tag_version}"
        
        # Create tag
        if not confirm_step(
            f"\n🏷️  Create git tag {tag_name} on release branch?",
            default=True,
            non_interactive=args.non_interactive or args.dry_run,
        ):
            print("⚠️  Skipping tag creation (user cancelled)")
            if not args.non_interactive:
                sys.exit(0)
        else:
            if not create_git_tag(tag_version, args.tag_message, dry_run=args.dry_run):
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
                if not push_tag(tag_version, dry_run=args.dry_run):
                    sys.exit(1)
        
        print("\n✅ Tag creation complete!")
        return
    
    # Handle version based on workflow type
    new_version = current_version
    
    # Version bumping happens in dev_to_main workflow (because main is protected)
    if workflow_type == "dev_to_main":
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
            # No version specified - prompt for bump type
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
    elif workflow_type == "main_to_release":
        # No version bump for main→release workflow (version already set in dev→main)
        print("ℹ️  Main→Release workflow: Version already set from dev→main merge")
    elif workflow_type == "release_tag":
        print("ℹ️  Release tag workflow: Use --tag flag to create tags")
        sys.exit(0)
    else:
        print(f"⚠️  Unknown workflow type: {workflow_type}")
        print("   Expected: dev, main, or release branch")
        sys.exit(1)
    
    # Update changelog BEFORE checking for commits (for dev_to_main workflow with version bump)
    if workflow_type == "dev_to_main" and new_version != current_version and not args.skip_changelog:
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
    
    # Check git status and auto-commit version changes if that's all that's changed
    if not args.dry_run:
        # For dev_to_main workflow, check if we can auto-commit version changes
        if workflow_type == "dev_to_main" and new_version != current_version:
            if not check_and_commit_version_changes(new_version, workflow_type, dry_run=args.dry_run):
                response = input("\nContinue with uncommitted changes? (y/N): ")
                if response.lower() != "y":
                    sys.exit(0)
        else:
            # For other workflows or no version change, use standard check
            if not check_git_status():
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
    
    # Update version (only if explicitly provided, not if it was bumped - bump already updated it)
    if workflow_type == "dev_to_main" and new_version != current_version and args.version:
        # Version was explicitly provided, update it (bump already handled it)
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
    
    # Commit and create PR based on workflow
    should_commit = False
    commit_message = ""
    
    if workflow_type == "dev_to_main" and new_version != current_version:
        # Commit version and changelog changes (version bump happens here)
        should_commit = True
        commit_message = f"Bump version to v{new_version} and prepare merge to main"
    elif workflow_type == "dev_to_main":
        # Commit any changes (even if no version bump)
        should_commit = True
        commit_message = "Prepare merge to main"
    elif workflow_type == "main_to_release":
        # Commit any changes for release (version already set from dev→main)
        should_commit = True
        commit_message = "Prepare release"
    
    if should_commit and not args.skip_pr:
        if workflow_type == "dev_to_main":
            # For dev→main, commit version and changelog changes if version was bumped
            if new_version != current_version:
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
            else:
                # No version bump, just commit any other changes
                if not confirm_step(
                    "\n💾 Commit changes for merge to main?",
                    default=True,
                    non_interactive=args.non_interactive or args.dry_run,
                ):
                    print("⚠️  Skipping commit (user cancelled)")
                    if not args.non_interactive:
                        sys.exit(0)
                else:
                    # Check if there are any changes to commit
                    try:
                        result = subprocess.run(
                            ["git", "status", "--porcelain"],
                            cwd=get_project_root(),
                            capture_output=True,
                            text=True,
                            check=True,
                        )
                        if result.stdout.strip():
                            subprocess.run(
                                ["git", "add", "-A"],
                                cwd=get_project_root(),
                                check=True,
                                capture_output=True,
                            )
                            subprocess.run(
                                ["git", "commit", "-m", commit_message],
                                cwd=get_project_root(),
                                check=True,
                                capture_output=True,
                            )
                            print(f"✅ Committed changes: {commit_message}")
                        else:
                            print("ℹ️  No changes to commit")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Failed to commit changes: {e}")
                        if not args.dry_run:
                            sys.exit(1)
        elif workflow_type == "main_to_release":
            # For main→release, commit any changes (version already set)
            if not confirm_step(
                "\n💾 Commit changes for release?",
                default=True,
                non_interactive=args.non_interactive or args.dry_run,
            ):
                print("⚠️  Skipping commit (user cancelled)")
                if not args.non_interactive:
                    sys.exit(0)
            else:
                # Check if there are any changes to commit
                try:
                    result = subprocess.run(
                        ["git", "status", "--porcelain"],
                        cwd=get_project_root(),
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    if result.stdout.strip():
                        subprocess.run(
                            ["git", "add", "-A"],
                            cwd=get_project_root(),
                            check=True,
                            capture_output=True,
                        )
                        subprocess.run(
                            ["git", "commit", "-m", commit_message],
                            cwd=get_project_root(),
                            check=True,
                            capture_output=True,
                        )
                        print(f"✅ Committed changes: {commit_message}")
                    else:
                        print("ℹ️  No changes to commit")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to commit changes: {e}")
                    if not args.dry_run:
                        sys.exit(1)
        
        # Push the branch and create PR (for both workflows)
        if should_commit and not args.skip_pr:
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
                    if target_branch:
                        if not confirm_step(
                            f"\n🔀 Create pull request to merge into '{target_branch}' branch?",
                            default=True,
                            non_interactive=args.non_interactive or args.dry_run,
                        ):
                            print("⚠️  Skipping PR creation (user cancelled)")
                            if not args.non_interactive:
                                sys.exit(0)
                        else:
                            pr_version = new_version if workflow_type == "dev_to_main" else current_version
                            pr_url = create_release_pr(
                                pr_version,
                                release_branch=target_branch,
                                workflow_type=workflow_type,
                                dry_run=args.dry_run,
                            )
                            if pr_url and not args.dry_run:
                                print(f"\n📌 PR created: {pr_url}")
                                # Optionally open the PR in browser
                                if not confirm_step(
                                    "\n🌐 Open PR in browser?",
                                    default=True,
                                    non_interactive=args.non_interactive,
                                ):
                                    print(f"   PR URL: {pr_url}")
                                else:
                                    try:
                                        import webbrowser
                                        webbrowser.open(pr_url)
                                        print(f"   Opened: {pr_url}")
                                    except Exception:
                                        print(f"   Could not open browser. PR URL: {pr_url}")
                                
                                if workflow_type == "dev_to_main":
                                    print("\n   After PR is merged to main, create a PR from main to release branch.")
                                elif workflow_type == "main_to_release":
                                    print("\n   After PR is merged to release branch, use --tag to create version tag.")
                                else:
                                    print("\n   Wait for the PR to be reviewed and merged.")
                            elif not args.dry_run:
                                # PR creation failed or was skipped
                                repo_info = get_remote_repo_info()
                                if repo_info:
                                    owner, repo = repo_info
                                    print(f"\n📝 PR not created. You can create it manually:")
                                    print(f"   https://github.com/{owner}/{repo}/compare/{target_branch}...{current_branch}")
    
    print("\n✅ Process complete!")
    
    if args.dry_run:
        print("\n[DRY RUN] No changes were made. Run without --dry-run to execute.")
    else:
        print(f"\n📌 Next steps:")
        if workflow_type == "dev_to_main":
            print(f"   1. Review and merge the PR from dev to main")
            print(f"   2. After merge, checkout main and prepare release:")
            print(f"      git checkout main")
            print(f"      python utilities/build_and_release.py")
        elif workflow_type == "main_to_release":
            print(f"   1. Review and merge the PR from main to release branch")
            print(f"   2. After merge, checkout release branch and create tag:")
            print(f"      git checkout release")
            print(f"      python utilities/build_and_release.py --tag")
        elif workflow_type == "release_tag":
            print(f"   Tag created! GitHub Actions should trigger automatically.")


if __name__ == "__main__":
    main()
