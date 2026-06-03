# Execute this statement.
from pathlib import Path
# Import sys.
import sys


# Define function base_dir.
def base_dir() -> Path:
    # Check condition and run block if true.
    if getattr(sys, 'frozen', False):
        # Return the computed value.
        return Path(sys.executable).parent
    # Return the computed value.
    return Path(__file__).resolve().parent


# Define function resource_path.
def resource_path(relative: str) -> Path:
    # Check condition and run block if true.
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Return the computed value.
        return Path(sys._MEIPASS) / relative
    # Return the computed value.
    return base_dir() / relative
