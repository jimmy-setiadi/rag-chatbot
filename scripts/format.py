#!/usr/bin/env python3
"""Code formatting script using Black and isort"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"Running {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout)
    else:
        print(f"✗ {description} failed")
        if result.stderr:
            print(result.stderr)
        return False
    return True

def format_code():
    """Format code using Black and isort"""
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    commands = [
        ("python -m isort backend/ --diff --check-only", "isort check"),
        ("python -m isort backend/", "isort formatting"),
        ("python -m black backend/ --diff --check", "black check"),
        ("python -m black backend/", "black formatting"),
    ]
    
    success = True
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            success = False
    
    return success

if __name__ == "__main__":
    success = format_code()
    sys.exit(0 if success else 1)