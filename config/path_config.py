from pathlib import Path

# ************ PROJECT ROOT ************
BASE_DIR = Path(__file__).resolve().parents[1]

# ************ LOGS ROOT *******************
LOGS_DIR = BASE_DIR / "logs"


# ************ DATA ************
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


