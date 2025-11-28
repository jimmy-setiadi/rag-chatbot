#!/usr/bin/env python3
"""Code quality check script"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*50}")
    print(f"Running {description}")
    print('='*50)
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print(f"✓ {description} passed")
    else:
        print(f"✗ {description} failed")
        return False
    return True

def quality_check():
    """Run all quality checks"""
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    checks = [
        ("python -m black backend/ --check --diff", "Black formatting check"),
        ("python -m isort backend/ --check-only --diff", "Import sorting check"),
        ("python -m flake8 backend/", "Flake8 linting"),
        ("python -m pytest backend/tests/ -v", "Test suite"),
    ]
    
    print("Starting code quality checks...")
    
    passed = 0
    total = len(checks)
    
    for cmd, desc in checks:
        if run_command(cmd, desc):
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Quality Check Results: {passed}/{total} passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All quality checks passed!")
        return True
    else:
        print("❌ Some quality checks failed")
        return False

if __name__ == "__main__":
    success = quality_check()
    sys.exit(0 if success else 1)