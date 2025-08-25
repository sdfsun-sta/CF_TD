"""Pytest configuration to ensure project root on sys.path."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
