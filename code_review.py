#!/usr/bin/env python3
"""
Code Review Automation Tool Entry Point

This script can be run from the root directory to execute code reviews.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.main import main

if __name__ == "__main__":
    main()