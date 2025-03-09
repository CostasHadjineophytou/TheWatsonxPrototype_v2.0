import os
import sys
from pathlib import Path

# Add both the project root and the backend directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Create necessary test output directories
test_output_dir = Path(project_root) / "data" / "audio" / "test_output"
e2e_output_dir = Path(project_root) / "data" / "audio" / "e2e_test_output"
test_samples_dir = Path(project_root) / "data" / "audio" / "test_samples"

# Ensure all test directories exist
for directory in [test_output_dir, e2e_output_dir, test_samples_dir]:
    directory.mkdir(parents=True, exist_ok=True)