#!/usr/bin/env python3
"""
Script to update the version using bump-my-version.
This script can be used to bump versions in both pyproject.toml and __init__.py files.
"""
import subprocess
import sys
from pathlib import Path
import click


def run_bump_version(project_root: Path, part: str, dry_run: bool = False) -> None:
    """Run bump-my-version to update the version."""
    cmd = ["bump-my-version", "bump", part]

    if dry_run:
        cmd.append("--dry-run")

    click.echo(f"🔄 Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )

        if dry_run:
            click.echo("📋 Dry run output:")
            click.echo(result.stdout)
        else:
            click.echo("✅ Version bumped successfully!")
            click.echo(result.stdout)

    except subprocess.CalledProcessError as e:
        click.secho(f"❌ Error running bump-my-version: {e}", fg="red")
        click.secho(f"stderr: {e.stderr}", fg="red")
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
    click.echo("📦 Installing bump-my-version...")

    try:
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
    pyproject_file = project_root / "pyproject.toml"

    if not pyproject_file.exists():
        click.secho("❌ pyproject.toml not found", fg="red")
        return

    try:
        result = subprocess.run(
            ["bump-my-version", "show", "current"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True
        )
        click.echo(f"📋 Current version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        click.secho(f"❌ Error getting current version: {e}", fg="red")
        click.secho(f"stderr: {e.stderr}", fg="red")


@click.group()
def cli() -> None:
    """CLI for updating project version using bump-my-version."""
    return None


@cli.command("show")
def show() -> None:
    """Show the current version."""
    project_root = Path(__file__).parent.parent
    if not check_bump_my_version_installed():
        click.secho("❌ bump-my-version is not installed", fg="red")
        if click.confirm("Would you like to install it now?"):
            install_bump_my_version()
        else:
            click.echo("Please install bump-my-version manually:")
            click.echo("  pip install bump-my-version")
            sys.exit(1)
    show_current_version(project_root)


@cli.command("bump")
@click.argument("part", type=click.Choice(["1", "2", "3"], case_sensitive=False))
@click.option("--dry-run", is_flag=True, help="Show what would be changed without making changes")
def bump(part: str, dry_run: bool) -> None:
    """Bump the version: 1=patch, 2=minor, 3=major."""
    project_root = Path(__file__).parent.parent

    if not check_bump_my_version_installed():
        click.secho("❌ bump-my-version is not installed", fg="red")
        if click.confirm("Would you like to install it now?"):
            install_bump_my_version()
        else:
            click.echo("Please install bump-my-version manually:")
            click.echo("  pip install bump-my-version")
            sys.exit(1)

    # Map numeric choice to version part
    version_parts = {
        "1": "patch",
        "2": "minor", 
        "3": "major"
    }
    
    version_part = version_parts[part]
    click.echo(f"🔧 Updating version ({version_part}) for TestRail API Module")
    click.echo(f"📁 Project root: {project_root}")

    run_bump_version(project_root, version_part, dry_run)

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