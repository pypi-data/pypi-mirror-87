from pathlib import Path

DRIVER_DIR = 'executor'
DRIVER_PATH = Path(__file__).parent.resolve() / DRIVER_DIR
if not DRIVER_PATH.exists():
    DRIVER_PATH.mkdir()
