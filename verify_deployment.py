"""
Streamlit Cloud Deployment Verification Script
This script checks if your app is ready for Streamlit Cloud deployment.
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists and is not empty."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 0:
            print(f"✅ {description}: Found ({size} bytes)")
            return True
        else:
            print(f"⚠️  {description}: Empty file!")
            return False
    else:
        print(f"❌ {description}: Not found!")
        return False

def check_python_version():
    """Check if running Python 3.11."""
    version = sys.version_info
    if version.major == 3 and version.minor == 11:
        print(f"✅ Python Version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"⚠️  Python Version: {version.major}.{version.minor}.{version.micro} (Expected 3.11.x)")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        num_files = len(os.listdir(dirpath))
        print(f"✅ {description}: Found ({num_files} items)")
        return True
    else:
        print(f"❌ {description}: Not found!")
        return False

def main():
    print("=" * 70)
    print("🚀 STREAMLIT CLOUD DEPLOYMENT READINESS CHECK")
    print("=" * 70)
    print()
    
    base_dir = Path(__file__).parent
    checks = []
    
    # Required files
    print("📄 Checking Required Files...")
    checks.append(check_file(base_dir / "streamlit_app.py", "Main App (streamlit_app.py)"))
    checks.append(check_file(base_dir / "requirements.txt", "Python Dependencies (requirements.txt)"))
    checks.append(check_file(base_dir / "packages.txt", "System Packages (packages.txt)"))
    checks.append(check_file(base_dir / ".python-version", "Python Version (.python-version)"))
    checks.append(check_file(base_dir / "runtime.txt", "Runtime Config (runtime.txt)"))
    print()
    
    # Optional but recommended
    print("📋 Checking Optional Files...")
    check_file(base_dir / "README.md", "README Documentation")
    check_file(base_dir / ".gitignore", "Git Ignore File")
    check_file(base_dir / ".streamlit" / "config.toml", "Streamlit Config")
    print()
    
    # Required directories
    print("📁 Checking Required Directories...")
    checks.append(check_directory(base_dir / "ml_model", "ML Model Directory"))
    checks.append(check_directory(base_dir / "ml_model" / "utils", "Utils Directory"))
    checks.append(check_directory(base_dir / "ml_model" / "data", "Data Directory"))
    print()
    
    # Python version
    print("🐍 Checking Python Environment...")
    check_python_version()
    print()
    
    # Check requirements.txt content
    print("📦 Checking Key Dependencies...")
    req_file = base_dir / "requirements.txt"
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            content = f.read()
            key_packages = [
                "streamlit",
                "opencv-python-headless",
                "mediapipe",
                "streamlit-webrtc",
                "numpy",
                "pandas"
            ]
            for pkg in key_packages:
                if pkg in content:
                    print(f"✅ {pkg}: Found")
                else:
                    print(f"❌ {pkg}: Missing!")
                    checks.append(False)
    print()
    
    # Check runtime.txt
    print("⚙️  Checking Runtime Configuration...")
    runtime_file = base_dir / "runtime.txt"
    if os.path.exists(runtime_file):
        with open(runtime_file, 'r') as f:
            runtime = f.read().strip()
            if "3.11" in runtime:
                print(f"✅ Runtime: {runtime}")
            else:
                print(f"⚠️  Runtime: {runtime} (Expected python-3.11.x)")
    print()
    
    # Check packages.txt
    print("🔧 Checking System Dependencies...")
    pkg_file = base_dir / "packages.txt"
    if os.path.exists(pkg_file):
        with open(pkg_file, 'r') as f:
            packages = f.read()
            if "libgl1" in packages or "libglib" in packages:
                print(f"✅ System packages configured for OpenCV")
            else:
                print(f"⚠️  Missing OpenCV system dependencies")
    print()
    
    # Final verdict
    print("=" * 70)
    if all(checks):
        print("🎉 ALL CHECKS PASSED! Your app is ready for Streamlit Cloud deployment!")
        print()
        print("Next steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://share.streamlit.io")
        print("3. Deploy your app")
        print("4. Share your public URL!")
    else:
        print("⚠️  SOME CHECKS FAILED! Please fix the issues above before deploying.")
        print()
        print("Review STREAMLIT_DEPLOYMENT.md for detailed instructions.")
    print("=" * 70)

if __name__ == "__main__":
    main()
