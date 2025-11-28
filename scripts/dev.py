#!/usr/bin/env python3
"""Development workflow script"""

import subprocess
import sys
import os

def run_dev_workflow():
    """Run complete development workflow"""
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("🚀 Starting development workflow...")
    
    # Format code
    print("\n1. Formatting code...")
    result = subprocess.run([sys.executable, "scripts/format.py"])
    if result.returncode != 0:
        print("❌ Formatting failed")
        return False
    
    # Run quality checks
    print("\n2. Running quality checks...")
    result = subprocess.run([sys.executable, "scripts/quality.py"])
    if result.returncode != 0:
        print("❌ Quality checks failed")
        return False
    
    print("\n✅ Development workflow completed successfully!")
    return True

if __name__ == "__main__":
    success = run_dev_workflow()
    sys.exit(0 if success else 1)