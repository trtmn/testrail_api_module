#!/usr/bin/env python3
"""
Script to update the version manually in pyproject.toml and __init__.py files.
This script can be used to bump versions in both pyproject.toml and __init__.py files.
"""
import re
import sys
from pathlib import Path
import click


def get_current_version(project_root: Path) -> str:
    """Get the current version from pyproject.toml."""
    pyproject_file = project_root / "pyproject.toml"
    
    if not pyproject_file.exists():
        click.secho("❌ pyproject.toml not found", fg="red")
        sys.exit(1)
    
    content = pyproject_file.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not match:
        click.secho("❌ Could not find version in pyproject.toml", fg="red")
        sys.exit(1)
    
    return match.group(1)


def bump_version(version: str, part: str) -> str:
    """Bump the version by the specified part."""
    parts = version.split('.')
    if len(parts) != 3:
        click.secho(f"❌ Invalid version format: {version}", fg="red")
        sys.exit(1)
    
    major, minor, patch = map(int, parts)
    
    if part == "patch":
        patch += 1
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        click.secho(f"❌ Invalid version part: {part}", fg="red")
        sys.exit(1)
    
    return f"{major}.{minor}.{patch}"


def update_file_version(file_path: Path, old_version: str, new_version: str, pattern: str, replacement: str) -> bool:
    """Update version in a file."""
    if not file_path.exists():
        click.secho(f"❌ File not found: {file_path}", fg="red")
        return False
    
    content = file_path.read_text()
    
    # Create the actual search and replace patterns
    search_pattern = pattern.format(current_version=old_version)
    replace_pattern = replacement.format(new_version=new_version)
    
    if search_pattern not in content:
        click.secho(f"❌ Version {old_version} not found in {file_path}", fg="red")
        return False
    
    new_content = content.replace(search_pattern, replace_pattern)
    file_path.write_text(new_content)
    
    click.echo(f"✅ Updated {file_path}")
    return True


def run_version_update(project_root: Path, part: str, dry_run: bool = False) -> None:
    """Update version in all configured files."""
    current_version = get_current_version(project_root)
    new_version = bump_version(current_version, part)
    
    click.echo(f"🔄 Updating version from {current_version} to {new_version}")
    
    if dry_run:
        click.echo("📋 Dry run - would update:")
        click.echo(f"  pyproject.toml: version = \"{current_version}\" → version = \"{new_version}\"")
        click.echo(f"  __init__.py: __version__ = '{current_version}' → __version__ = '{new_version}'")
        return
    
    # Update pyproject.toml
    pyproject_file = project_root / "pyproject.toml"
    update_file_version(
        pyproject_file,
        current_version,
        new_version,
        'version = "{current_version}"',
        'version = "{new_version}"'
    )
    
    # Update __init__.py
    init_file = project_root / "src" / "testrail_api_module" / "__init__.py"
    update_file_version(
        init_file,
        current_version,
        new_version,
        "__version__ = '{current_version}'",
        "__version__ = '{new_version}'"
    )
    
    click.echo(f"✅ Version updated to {new_version}")


def check_bump_my_version_installed() -> bool:
    """Check if bump-my-version is installed."""
    try:
        import subprocess
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
    click.echo("📦 Installing bump-my-version...")

    try:
        import subprocess
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "bump-my-version"],
            check=True,
            capture_output=True,
            text=True
        )
        click.echo("✅ bump-my-version installed successfully!")
    except subprocess.CalledProcessError as e:
        click.secho(f"❌ Error installing bump-my-version: {e}", fg="red")
        click.secho(f"stderr: {e.stderr}", fg="red")
        sys.exit(1)


def show_current_version(project_root: Path) -> None:
    """Show the current version from pyproject.toml."""
    version = get_current_version(project_root)
    click.echo(f"📋 Current version: {version}")


@click.group()
def cli() -> None:
    """CLI for updating project version."""
    return None


@cli.command("show")
def show() -> None:
    """Show the current version."""
    project_root = Path(__file__).parent.parent
    show_current_version(project_root)


@cli.command("bump")
@click.argument("part", type=click.Choice(["1", "2", "3"], case_sensitive=False))
@click.option("--dry-run", is_flag=True, help="Show what would be changed without making changes")
def bump(part: str, dry_run: bool) -> None:
    """Bump the version: 1=patch, 2=minor, 3=major."""
    project_root = Path(__file__).parent.parent

    # Map numeric choice to version part
    version_parts = {
        "1": "patch",
        "2": "minor", 
        "3": "major"
    }
    
    version_part = version_parts[part]
    click.echo(f"🔧 Updating version ({version_part}) for TestRail API Module")
    click.echo(f"📁 Project root: {project_root}")

    run_version_update(project_root, version_part, dry_run)

    if not dry_run:
        click.echo("\n🎉 Version update completed!")
        click.echo("📋 Next steps:")
        click.echo("   1. Review the changes")
        click.echo("   2. Run tests to ensure everything works")
        click.echo("   3. Commit the changes")
        click.echo("   4. Generate documentation with new version")
        click.echo("   5. Create a release tag")


if __name__ == "__main__":
    cli()