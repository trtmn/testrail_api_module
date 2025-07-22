#!/usr/bin/env python3
"""
Script to generate library stubs for the TestRail API module using stubgen.
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
        # Generate stubs in a temporary directory first
        temp_dir = project_root / "temp_stubs"
        temp_dir.mkdir(exist_ok=True)
        
        # Generate stubs for the entire package
        subprocess.run(
            [
                "stubgen",
                "--output",
                str(temp_dir),
                str(src_dir),
                "--include-docstrings",
                "--include-private",
            ],
            check=True,
            capture_output=True,
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
        print(f"❌ Error generating stubs: {e}")
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
        with open(stub_file, 'r') as f:
            content = f.read()
        
        # Replace common issues in stubs
        improvements = [
            # Replace Incomplete with proper types
            ("from _typeshed import Incomplete", "from typing import Any, Optional, Dict, List"),
            (": Incomplete", ": Any"),
            ("client: Incomplete", "client: Any"),
            ("logger: Incomplete", "logger: Any"),
            
            # Fix common method signatures
            ("def __init__(self, client) -> None:", "def __init__(self, client: Any) -> None:"),
            
            # Add proper type annotations for common API methods
            ("def _api_request(self, method, endpoint, data=None, **kwargs):", 
             "def _api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:"),
            
            # Add proper return types for other API methods
            ("def _api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:", 
             "def _api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:"),
        ]
        
        for old, new in improvements:
            content = content.replace(old, new)
        
        # Write improved content back
        with open(stub_file, 'w') as f:
            f.write(content)
            
        print(f"🔧 Improved: {stub_file.name}")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not improve {stub_file.name}: {e}")


def update_pyproject_toml(project_root: Path) -> None:
    """Update pyproject.toml to include mypy configuration and stub generation."""
    pyproject_file = project_root / "pyproject.toml"
    
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return
    
    # Read current content
    with open(pyproject_file, 'r') as f:
        content = f.read()
    
    # Check if mypy configuration already exists
    if "[tool.mypy]" in content:
        print("ℹ️  mypy configuration already exists in pyproject.toml")
        return
    
    # Add mypy configuration
    mypy_config = """

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Allow untyped defs for now
disallow_incomplete_defs = false  # Allow incomplete defs for now
check_untyped_defs = true
disallow_untyped_decorators = false  # Allow untyped decorators for now
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

# Include stubs in the package
[tool.setuptools.package-data]
testrail_api_module = ["*.pyi", "py.typed"]
"""
    
    # Append mypy configuration
    with open(pyproject_file, 'a') as f:
        f.write(mypy_config)
    
    print("✅ Added mypy configuration to pyproject.toml")


def add_stub_generation_to_dev_deps(project_root: Path) -> None:
    """Add stubgen to development dependencies if not already present."""
    pyproject_file = project_root / "pyproject.toml"
    
    if not pyproject_file.exists():
        print("❌ pyproject.toml not found")
        return
    
    # Read current content
    with open(pyproject_file, 'r') as f:
        content = f.read()
    
    # Check if stubgen is already in dev dependencies
    if "stubgen" in content:
        print("ℹ️  stubgen already in development dependencies")
        return
    
    # Find the dev dependencies section and add stubgen
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip() == 'dev = [':
            # Find the closing bracket
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == ']':
                    # Insert stubgen before the closing bracket
                    lines.insert(j, '    "stubgen",')
                    break
            break
    
    # Write updated content
    with open(pyproject_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print("✅ Added stubgen to development dependencies")





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
    
    # Update pyproject.toml
    update_pyproject_toml(project_root)
    add_stub_generation_to_dev_deps(project_root)
    

    
    print("\n🎉 Library stubs generation completed!")
    print("📋 Next steps:")
    print("   1. Review generated .pyi files in src/testrail_api_module/")
    print("   2. Manually improve type annotations if needed")
    print("   3. Run 'mypy src/testrail_api_module' to check types")
    print("   4. Run 'python utilities/generate_stubs.py' to regenerate stubs after code changes")
    print("   5. Commit the .pyi files and py.typed to version control")


if __name__ == "__main__":
    main() 