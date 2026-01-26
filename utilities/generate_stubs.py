#!/usr/bin/env python3
"""
Script to generate library stubs for the TestRail API module using stubgen.

Note: On some Python versions/platforms, `mypy` may be installed as compiled
extension modules (mypy+mypyc). In that case, `python -m mypy.stubgen` cannot
run because there is no Python code object available. The `stubgen` console
script still works, so we use that.
Library stubs (.pyi files) provide type information for better IDE support and static type checking.
"""
import subprocess
import sys
import shutil
from pathlib import Path



def clean_existing_stubs(project_root: Path) -> None:
    """Clean up existing stub files in the source directory."""
    src_dir = project_root / "src" / "testrail_api_module"
    
    # Remove existing .pyi files
    pyi_files = list(src_dir.glob("*.pyi"))
    for pyi_file in pyi_files:
        pyi_file.unlink()
        print(f"🧹 Removed: {pyi_file.name}")
    
    if pyi_files:
        print(f"✅ Cleaned up {len(pyi_files)} existing stub files")
    else:
        print("ℹ️  No existing stub files to clean")


def generate_stubs(project_root: Path) -> None:
    """Generate library stubs using stubgen."""
    src_dir = project_root / "src" / "testrail_api_module"
    
    print("Generating library stubs with stubgen...")
    
    try:
        # Try to find stubgen executable first
        stubgen_executable = shutil.which("stubgen")
        
        # If not found, try to use python -m mypy.stubgen
        if not stubgen_executable:
            # Check if we're in a virtual environment
            venv_python = project_root / ".venv" / "bin" / "python"
            if venv_python.exists():
                python_executable = str(venv_python)
            else:
                python_executable = sys.executable
            
            # Try to import mypy to verify it's available
            try:
                import mypy.stubgen  # pyright: ignore[reportMissingImports]
                stubgen_executable = python_executable
                stubgen_args = ["-m", "mypy.stubgen"]
            except ImportError:
                print(
                    "❌ Error generating stubs: 'mypy' not found. "
                    "Install the dev dependencies (includes 'mypy'), e.g. "
                    "`uv sync --extra dev`."
                )
                sys.exit(1)
        else:
            stubgen_args = []

        # Generate stubs in a temporary directory first
        temp_dir = project_root / "temp_stubs"
        temp_dir.mkdir(exist_ok=True)
        
        # Build the command
        cmd = [stubgen_executable] + stubgen_args + [
            "--output",
            str(temp_dir),
            str(src_dir),
            "--include-docstrings",
            "--include-private",
        ]
        
        # Generate stubs for the entire package
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
        
        # Copy stubs from nested directory to the correct location
        nested_dir = temp_dir / "testrail_api_module"
        if nested_dir.exists():
            for pyi_file in nested_dir.glob("*.pyi"):
                target_path = src_dir / pyi_file.name
                shutil.copy2(pyi_file, target_path)
                print(f"📄 Generated: {pyi_file.name}")
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        print("✅ Library stubs generated successfully!")
        
    except subprocess.CalledProcessError as e:
        stderr = ""
        stdout = ""
        if getattr(e, "stderr", None):
            stderr = e.stderr.strip()
        if getattr(e, "stdout", None):
            stdout = e.stdout.strip()
        
        error_msg = f"❌ Error generating stubs (exit code {e.returncode})"
        if stderr:
            error_msg += f":\n{stderr}"
        elif stdout:
            error_msg += f":\n{stdout}"
        else:
            error_msg += f": {e}"
        print(error_msg)
        sys.exit(1)
    except FileNotFoundError as e:
        print(
            f"❌ Error: Required executable not found: {e}\n"
            "Install the dev dependencies (includes 'mypy'), e.g. "
            "`uv sync --extra dev`."
        )
        sys.exit(1)





def create_py_typed_file(project_root: Path) -> None:
    """Create a py.typed file to indicate this package supports typing."""
    py_typed_file = project_root / "src" / "testrail_api_module" / "py.typed"
    
    if not py_typed_file.exists():
        py_typed_file.touch()
        print(f"📝 Created: {py_typed_file}")
    else:
        print(f"📝 Already exists: {py_typed_file}")


def improve_stubs(project_root: Path) -> None:
    """Improve generated stubs with better type annotations."""
    src_dir = project_root / "src" / "testrail_api_module"
    
    print("Improving generated stubs...")
    
    # List of stub files to improve
    stub_files = list(src_dir.glob("*.pyi"))
    
    for stub_file in stub_files:
        improve_single_stub(stub_file)
    
    print(f"✅ Improved {len(stub_files)} stub files")


def improve_single_stub(stub_file: Path) -> None:
    """Improve a single stub file with better type annotations."""
    try:
        with open(stub_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace common issues in stubs
        improvements = [
            # Replace Incomplete with proper types
            (
                "from _typeshed import Incomplete",
                "from typing import Any, Optional, Dict, List",
            ),
            (": Incomplete", ": Any"),
            ("client: Incomplete", "client: Any"),
            ("logger: Incomplete", "logger: Any"),
            
            # Fix common method signatures
            (
                "def __init__(self, client) -> None:",
                "def __init__(self, client: Any) -> None:",
            ),
            
            # Add proper type annotations for common API methods
            (
                "def _api_request(self, method, endpoint, data=None, **kwargs):",
                "def _api_request(self, method: str, endpoint: str, "
                "data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> "
                "Optional[Dict[str, Any]]:",
            ),
            
            # Add proper return types for other API methods
            (
                "def _api_request(self, method: str, endpoint: str, "
                "data: Optional[Dict[str, Any]] = None) -> Any:",
                "def _api_request(self, method: str, endpoint: str, "
                "data: Optional[Dict[str, Any]] = None) -> "
                "Optional[Dict[str, Any]]:",
            ),
        ]
        
        for old, new in improvements:
            content = content.replace(old, new)
        
        # Write improved content back
        with open(stub_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"🔧 Improved: {stub_file.name}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not improve {stub_file.name}: {e}")


def main() -> None:
    """Main function to generate library stubs."""
    # Get the project root directory (utilities/../)
    project_root = Path(__file__).parent.parent
    
    print("🔧 Generating library stubs for TestRail API Module")
    print(f"📁 Project root: {project_root}")
    
    # Clean up existing stubs
    clean_existing_stubs(project_root)
    
    # Generate new stubs
    generate_stubs(project_root)
    
    # Improve the stubs
    improve_stubs(project_root)
    
    # Create py.typed file
    create_py_typed_file(project_root)
    
    # Note: This script does not modify pyproject.toml. Keep stub tooling
    # dependencies in `pyproject.toml`'s dev extras.

    print("\n🎉 Library stubs generation completed!")
    print("📋 Next steps:")
    print("   1. Review generated .pyi files in src/testrail_api_module/")
    print("   2. Manually improve type annotations if needed")
    print("   3. Run 'mypy src/testrail_api_module' to check types")
    print("   4. Run 'python utilities/generate_stubs.py' to regenerate stubs after code changes")
    print("   5. Commit the .pyi files and py.typed to version control")


if __name__ == "__main__":
    main() 