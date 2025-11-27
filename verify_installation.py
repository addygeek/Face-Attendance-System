#!/usr/bin/env python3
"""
Face Attendance System - Installation Verification Script
Verifies all dependencies are installed correctly for Python 3.11+
"""

import sys
import subprocess
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{text:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ {text}{RESET}")

def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print(f"Python Version: {version_str}")
    
    if version.major == 3 and version.minor >= 11:
        print_success(f"Python {version_str} is compatible (3.11+)")
        return True
    else:
        print_error(f"Python {version_str} is not compatible (requires 3.11+)")
        return False

def check_pip_version():
    """Check pip version"""
    print_header("Pip Version Check")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        pip_version = result.stdout.strip()
        print(pip_version)
        print_success("Pip is installed")
        return True
    except Exception as e:
        print_error(f"Pip check failed: {e}")
        return False

def check_virtual_environment():
    """Check if running in virtual environment"""
    print_header("Virtual Environment Check")
    
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print_success(f"Running in virtual environment: {sys.prefix}")
        return True
    else:
        print_warning("Not running in virtual environment")
        print_info("Recommended: Create virtual environment with:")
        print_info("  Windows: python -m venv .venv && .venv\\Scripts\\activate")
        print_info("  Mac/Linux: python3 -m venv .venv && source .venv/bin/activate")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print_success(f"{package_name:20} {version}")
        return True
    except ImportError:
        print_error(f"{package_name:20} NOT INSTALLED")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print_header("Dependency Check")
    
    dependencies = [
        ("numpy", "numpy"),
        ("opencv-python", "cv2"),
        ("flask", "flask"),
        ("flask-cors", "flask_cors"),
        ("mediapipe", "mediapipe"),
    ]
    
    results = {}
    for package_name, import_name in dependencies:
        results[package_name] = check_package(package_name, import_name)
    
    return results

def check_optional_packages():
    """Check optional packages"""
    print_header("Optional Packages Check")
    
    optional = [
        ("pytest", "pytest"),
        ("gunicorn", "gunicorn"),
        ("python-dotenv", "dotenv"),
    ]
    
    for package_name, import_name in optional:
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            print_info(f"{package_name:20} {version} (optional)")
        except ImportError:
            print_info(f"{package_name:20} not installed (optional)")

def check_project_structure():
    """Check project structure"""
    print_header("Project Structure Check")
    
    required_dirs = [
        "ml_model",
        "web_app",
        "data",
    ]
    
    required_files = [
        "ml_model/app.py",
        "ml_model/requirements.txt",
        "web_app/index.html",
        "web_app/script.js",
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print_success(f"Directory: {dir_name}/")
        else:
            print_error(f"Directory: {dir_name}/ NOT FOUND")
            all_ok = False
    
    for file_name in required_files:
        if Path(file_name).exists():
            print_success(f"File: {file_name}")
        else:
            print_error(f"File: {file_name} NOT FOUND")
            all_ok = False
    
    return all_ok

def check_api_health():
    """Check if API is running"""
    print_header("API Health Check")
    
    try:
        import requests
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                print_success("API is running on http://localhost:5000")
                return True
        except requests.exceptions.ConnectionError:
            print_warning("API is not running (this is normal if not started)")
            print_info("Start API with: python ml_model/app.py")
            return False
    except ImportError:
        print_warning("requests library not installed (needed for API check)")
        return False

def generate_report(results):
    """Generate final report"""
    print_header("Installation Report")
    
    total = len(results)
    installed = sum(1 for v in results.values() if v)
    
    print(f"Total Packages: {total}")
    print(f"Installed: {GREEN}{installed}{RESET}")
    print(f"Missing: {RED}{total - installed}{RESET}")
    
    if installed == total:
        print_success("All dependencies are installed!")
        return True
    else:
        print_error("Some dependencies are missing!")
        print_info("Install missing packages with:")
        print_info("  pip install -r ml_model/requirements.txt")
        return False

def main():
    """Main verification function"""
    print(f"\n{BOLD}{BLUE}Face Attendance System - Installation Verification{RESET}")
    print(f"{BOLD}{BLUE}Python 3.11+ Deployment{RESET}\n")
    
    # Run checks
    python_ok = check_python_version()
    pip_ok = check_pip_version()
    venv_ok = check_virtual_environment()
    deps = check_dependencies()
    check_optional_packages()
    structure_ok = check_project_structure()
    check_api_health()
    
    # Generate report
    report_ok = generate_report(deps)
    
    # Final summary
    print_header("Summary")
    
    if python_ok and pip_ok and report_ok and structure_ok:
        print_success("✓ System is ready for deployment!")
        print_info("Next steps:")
        print_info("  1. Start backend: python ml_model/app.py")
        print_info("  2. Open web_app/index.html in browser")
        print_info("  3. Allow camera access")
        print_info("  4. Start detecting faces!")
        return 0
    else:
        print_error("✗ System is not ready for deployment")
        print_info("Please fix the issues above and try again")
        return 1

if __name__ == "__main__":
    sys.exit(main())
