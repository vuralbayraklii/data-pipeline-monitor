"""Pytest configuration - Add app to path."""
import sys
from pathlib import Path

# Add apps/backend to Python path
backend_path = Path(__file__).parent.parent / "apps" / "backend"
sys.path.insert(0, str(backend_path))
