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


def get_next_version(current_version: str, bump_type: str) -> str:
    """Calculate the next version based on current version and bump type."""
    if current_version == "unknown":
        return "unknown"
    
    try:
        # Parse current version
        parts = current_version.split('.')
        if len(parts) != 3:
            return "unknown"
        
        major, minor, patch = map(int, parts)
        
        if bump_type == "patch":
            return f"{major}.{minor}.{patch + 1}"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        elif bump_type == "major":
            return f"{major + 1}.0.0"
        else:
            return "unknown"
    except (ValueError, IndexError):
        return "unknown"


def update_version() -> bool:
    """Prompt user to update version and run update_version.py."""
    current_version = get_current_version()

    console.print(f"\n📋 Current version: [bold]{current_version}[/bold]")

    if not Confirm.ask("Would you like to update the version?"):
        return False

    # Ask for version update method
    console.print("\n[bold]Version update options:[/bold]")
    console.print("1. [cyan]Automatic bump[/cyan] - increment current version")
    console.print("2. [cyan]Manual version[/cyan] - specify exact version")

    method = Prompt.ask(
        "Choose version update method",
        choices=["1", "2"],
        default="1",
    )

    if method == "1":
        # Automatic version bump
        console.print("\n[bold]Version bump options:[/bold]")
        console.print(f"1. [cyan]patch[/cyan] - for bug fixes ({current_version} → {get_next_version(current_version, 'patch')})")
        console.print(f"2. [cyan]minor[/cyan] - for new features ({current_version} → {get_next_version(current_version, 'minor')})")
        console.print(f"3. [cyan]major[/cyan] - for breaking changes ({current_version} → {get_next_version(current_version, 'major')})")

        part = Prompt.ask(
            "Choose version bump type",
            choices=["1", "2", "3"],
            default="1",
        )

        # Map choice to version part
        part_map = {"1": "patch", "2": "minor", "3": "major"}
        version_part = part_map[part]

        console.print(f"\n🔄 Updating version ({version_part})...")

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

            # Get the updated version
            updated_version = get_current_version()
            
            console.print("✅ Version updated successfully!", style="green")
            console.print(f"📋 New version: [bold]{updated_version}[/bold]")
            console.print(result.stdout)
            return True

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Error updating version: {e}", style="red")
            console.print(f"stderr: {e.stderr}", style="red")
            return False

    else:
        # Manual version specification
        new_version = Prompt.ask(
            "Enter the new version (e.g., 1.0.0)",
            default=""
        )
        
        if not new_version:
            console.print("❌ No version specified", style="red")
            return False

        console.print(f"\n🔄 Setting version to {new_version}...")

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Setting version...", total=None)

                result = subprocess.run(
                    ["python", "utilities/update_version.py", "set", new_version],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                progress.update(task, completed=True)

            console.print("✅ Version set successfully!", style="green")
            console.print(f"📋 New version: [bold]{new_version}[/bold]")
            console.print(result.stdout)
            return True

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Error setting version: {e}", style="red")
            console.print(f"stderr: {e.stderr}", style="red")
            return False


def clean_build_artifacts() -> None:
    """Clean previous build artifacts for current version only."""
    console.print("🧹 Cleaning build artifacts for current version...", style="blue")
    
    current_version = get_current_version()
    if current_version == "unknown":
        console.print("⚠️  Could not determine current version, skipping cleanup", style="yellow")
        return

    # Clean build directory (always safe to remove)
    build_dir = Path("build")
    if build_dir.exists():
        console.print(f"  Removing: {build_dir}")
        subprocess.run(["rm", "-rf", str(build_dir)], check=True)

    # Clean egg-info directories for current version only
    for egg_info in Path(".").glob("*.egg-info"):
        if egg_info.is_dir():
            console.print(f"  Removing: {egg_info}")
            subprocess.run(["rm", "-rf", str(egg_info)], check=True)

    # Clean dist files for current version only
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file_path in dist_dir.glob("*"):
            if file_path.is_file():
                filename = file_path.name
                # Check if file contains current version
                if current_version in filename:
                    console.print(f"  Removing: {filename}")
                    file_path.unlink()
                else:
                    console.print(f"  Preserving: {filename} (different version)", style="green")


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


def test_built_package() -> bool:
    """Test the built wheel by installing it and running tests."""
    console.print("\n🧪 Testing built package...", style="blue")
    
    dist_dir = Path("dist")
    if not dist_dir.exists():
        console.print("❌ No dist directory found", style="red")
        return False
    
    # Find the wheel file
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        console.print("❌ No wheel files found in dist directory", style="red")
        return False
    
    wheel_file = wheel_files[0]  # Use the first wheel file
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Installing built wheel...", total=None)
            
            # Install the wheel in a temporary environment or uninstall first
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--force-reinstall", str(wheel_file)],
                capture_output=True,
                text=True,
                check=True,
            )
            
            progress.update(task, completed=True)
        
        console.print("✅ Built package installed successfully!", style="green")
        
        # Run tests against the installed package
        task = progress.add_task("Running tests against installed package...", total=None)
        
        result = subprocess.run(
            ["python", "utilities/run_tests.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        
        progress.update(task, completed=True)
        
        console.print("✅ Tests passed against installed package!", style="green")
        console.print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Error testing built package: {e}", style="red")
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
        "--skip-version",
        action="store_true",
        help="Skip version update prompts",
    )
    parser.add_argument(
        "--skip-wheel-test",
        action="store_true",
        help="Skip testing the built wheel",
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
        update_version()



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



    # Clean previous builds
    clean_build_artifacts()

    # Build package
    if not build_package():
        console.print("❌ Build failed!", style="red")
        sys.exit(1)

    # Test the built package
    if not args.skip_wheel_test:
        if args.non_interactive or Confirm.ask("Would you like to test the built package?"):
            if not test_built_package():
                if not args.non_interactive and not Confirm.ask("Built package test failed. Continue anyway?"):
                    sys.exit(1)
        else:
            console.print("⚠️  Skipping built package test...", style="yellow")

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
    