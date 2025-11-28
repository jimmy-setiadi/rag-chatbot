#!/usr/bin/env python3
"""
Test runner script for the RAG system
Usage: python run_tests.py [test_type]
"""

import subprocess
import sys
import os

def run_tests(test_type="all"):
    """Run tests based on type"""
    
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    commands = {
        "unit": ["python", "-m", "pytest", "tests/", "-m", "unit", "-v"],
        "api": ["python", "-m", "pytest", "tests/", "-m", "api", "-v"],
        "integration": ["python", "-m", "pytest", "tests/", "-m", "integration", "-v"],
        "all": ["python", "-m", "pytest", "tests/", "-v"],
        "coverage": ["python", "-m", "pytest", "tests/", "--cov=.", "--cov-report=html"]
    }
    
    if test_type not in commands:
        print(f"Invalid test type: {test_type}")
        print(f"Available types: {list(commands.keys())}")
        return 1
    
    print(f"Running {test_type} tests...")
    result = subprocess.run(commands[test_type])
    return result.returncode

if __name__ == "__main__":
    test_type = sys.argv[1] if len(sys.argv) > 1 else "all"
    exit_code = run_tests(test_type)
    sys.exit(exit_code)