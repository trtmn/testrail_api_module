#!/usr/bin/env python3
"""
Build script for the TestRail API module.
This script handles building, version management, and deployment preparation.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def check_dependencies() -> bool:
    """Check if all required dependencies are installed."""
    console.print("🔍 Checking dependencies...", style="blue")

    required_packages = [
        "build",
        "wheel",
        "setuptools",
        "rich",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        console.print(
            f"❌ Missing packages: {', '.join(missing_packages)}", style="red"
        )
        console.print(
            "Please install missing packages with: pip install "
            + " ".join(missing_packages),
            style="yellow",
        )
        return False

    console.print("✅ All dependencies are installed", style="green")
    return True


def get_current_version() -> str:
    """Get the current version from pyproject.toml."""
    try:
        result = subprocess.run(
            ["python", "utilities/update_version.py", "show"],
            capture_output=True,
            text=True,
            check=True,
        )
        # Extract version from output like "📋 Current version: 0.2.3"
        output = result.stdout.strip()
        if "Current version:" in output:
            return output.split("Current version:")[1].strip()
        return "unknown"
    except subprocess.CalledProcessError:
        return "unknown"


def update_version() -> bool:
    """Prompt user to update version and run update_version.py."""
    current_version = get_current_version()

    console.print(f"\n📋 Current version: [bold]{current_version}[/bold]")

    if not Confirm.ask("Would you like to update the version?"):
        return False

    console.print("\n[bold]Version bump options:[/bold]")
    console.print("1. [cyan]patch[/cyan] - for bug fixes (0.2.0 → 0.2.1)")
    console.print("2. [cyan]minor[/cyan] - for new features (0.2.0 → 0.3.0)")
    console.print("3. [cyan]major[/cyan] - for breaking changes (1.0.0 → 2.0.0)")

    part = Prompt.ask(
        "Choose version bump type",
        choices=["1", "2", "3"],
        default="1",
    )

    console.print(f"\n🔄 Updating version ({part})...")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running version update...", total=None)

            result = subprocess.run(
                ["python", "utilities/update_version.py", "bump", part],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

        console.print("✅ Version updated successfully!", style="green")
        console.print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Error updating version: {e}", style="red")
        console.print(f"stderr: {e.stderr}", style="red")
        return False


def clean_build_artifacts() -> None:
    """Clean previous build artifacts."""
    console.print("🧹 Cleaning build artifacts...", style="blue")

    build_dirs = ["build", "dist", "*.egg-info"]

    for pattern in build_dirs:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                console.print(f"  Removing: {path}")
                subprocess.run(["rm", "-rf", str(path)], check=True)


def run_tests() -> bool:
    """Run the test suite."""
    console.print("\n🧪 Running tests...", style="blue")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running test suite...", total=None)

            result = subprocess.run(
                ["python", "utilities/run_tests.py"],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

        console.print("✅ Tests passed!", style="green")
        console.print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Tests failed: {e}", style="red")
        console.print(f"stderr: {e.stderr}", style="red")
        return False


def generate_documentation() -> bool:
    """Generate documentation."""
    console.print("\n📚 Generating documentation...", style="blue")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating docs...", total=None)

            result = subprocess.run(
                ["python", "utilities/generate_docs.py"],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

        console.print("✅ Documentation generated!", style="green")
        console.print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Error generating documentation: {e}", style="red")
        console.print(f"stderr: {e.stderr}", style="red")
        return False


def generate_stubs() -> bool:
    """Generate type stubs."""
    console.print("\n🔧 Generating type stubs...", style="blue")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating stubs...", total=None)

            result = subprocess.run(
                ["python", "utilities/generate_stubs.py"],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

        console.print("✅ Type stubs generated!", style="green")
        console.print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Error generating stubs: {e}", style="red")
        console.print(f"stderr: {e.stderr}", style="red")
        return False


def build_package() -> bool:
    """Build the package using build."""
    console.print("\n📦 Building package...", style="blue")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Building package...", total=None)

            result = subprocess.run(
                [sys.executable, "-m", "build"],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, completed=True)

        console.print("✅ Package built successfully!", style="green")
        console.print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Build failed: {e}", style="red")
        console.print(f"stderr: {e.stderr}", style="red")
        return False


def show_build_summary() -> None:
    """Show a summary of the build artifacts."""
    console.print("\n📊 Build Summary", style="bold blue")

    dist_dir = Path("dist")
    if dist_dir.exists():
        table = Table(title="Generated Artifacts")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="green")

        for file_path in dist_dir.glob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                size_str = f"{size / 1024:.1f} KB"
                table.add_row(file_path.name, size_str)

        console.print(table)
    else:
        console.print("❌ No build artifacts found", style="red")


def main() -> None:
    """Main build function."""
    parser = argparse.ArgumentParser(
        description="Build script for TestRail API module"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run in non-interactive mode (skip all prompts)",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests",
    )
    parser.add_argument(
        "--skip-docs",
        action="store_true",
        help="Skip generating documentation",
    )
    parser.add_argument(
        "--skip-stubs",
        action="store_true",
        help="Skip generating type stubs",
    )
    parser.add_argument(
        "--skip-version",
        action="store_true",
        help="Skip version update prompts",
    )

    args = parser.parse_args()

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    console.print(
        Panel.fit(
            "[bold blue]TestRail API Module Build Script[/bold blue]\n"
            "This script will build the package and prepare it for distribution.",
            title="🚀 Build Process",
        )
    )

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Ask about version update
    if not args.skip_version:
        if update_version():
            # If version was updated, automatically regenerate docs and stubs
            console.print(
                "\n🔄 Version updated - regenerating docs and stubs...", style="blue"
            )

            if not args.skip_docs:
                if not generate_documentation():
                    console.print(
                        "⚠️  Documentation generation failed", style="yellow"
                    )
                else:
                    console.print(
                        "✅ Documentation regenerated with new version", style="green"
                    )

            if not args.skip_stubs:
                if not generate_stubs():
                    console.print("⚠️  Stub generation failed", style="yellow")
                else:
                    console.print(
                        "✅ Type stubs regenerated with new version", style="green"
                    )

    # Run tests
    if not args.skip_tests:
        if args.non_interactive or Confirm.ask("Would you like to run tests?"):
            if not run_tests():
                if (
                    not args.non_interactive
                    and not Confirm.ask("Tests failed. Continue with build?")
                ):
                    sys.exit(1)
        else:
            console.print("⚠️  Skipping tests...", style="yellow")

    # Generate documentation
    if not args.skip_docs:
        if args.non_interactive or Confirm.ask(
            "Would you like to generate documentation?"
        ):
            if not generate_documentation():
                console.print("⚠️  Documentation generation failed", style="yellow")
        else:
            console.print("⚠️  Skipping documentation...", style="yellow")

    # Generate stubs
    if not args.skip_stubs:
        if args.non_interactive or Confirm.ask(
            "Would you like to generate type stubs?"
        ):
            if not generate_stubs():
                console.print("⚠️  Stub generation failed", style="yellow")
        else:
            console.print("⚠️  Skipping stubs...", style="yellow")

    # Clean previous builds
    clean_build_artifacts()

    # Build package
    if not build_package():
        console.print("❌ Build failed!", style="red")
        sys.exit(1)

    # Show summary
    show_build_summary()

    console.print(
        Panel.fit(
            "[bold green]🎉 Build completed successfully![/bold green]\n\n"
            "Next steps:\n"
            "• Review the generated artifacts in the 'dist' directory\n"
            "• Test the package installation\n"
            "• Upload to PyPI if ready for release",
            title="✅ Success",
        )
    )


if __name__ == "__main__":
    main()
    