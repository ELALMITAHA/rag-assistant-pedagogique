import os
import re
import shutil
from pathlib import Path

from config.path_config import PROCESSED_DIR, RAW_DIR
from utils.logger import logger


# ***** HELPERS *****

import unicodedata

def clean_text(text: str) -> str:
    text = text.lower()
    
    # remove accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    return text

def extract_year(text: str) -> str:
    match = re.search(r"(20\d{2})", text)
    return match.group(1) if match else "unknown"

def detect_niveau(name: str) -> str:
    if "cycle" in name:
        return "college"
    return "lycee"

def detect_classe(name: str) -> str:
    name = clean_text(name)

    if "seconde" in name:
        return "seconde"
    if "premiere" in name:
        return "premiere"
    if "terminale" in name:
        return "terminale"
    if re.search(r"cycle[\s\-]?3", name):
        return "cycle3"
    if re.search(r"cycle[\s\-]?4", name):
        return "cycle4"

    return "unknown"

def detect_filiere(name: str) -> str:
    name = clean_text(name)

    if "generale et technologique" in name:
        return "generale_technologique"
    if "technologique" in name:
        return "technologique"
    if "generale" in name:
        return "generale"

    return "unknown"


def detect_option(name: str) -> str:
    if "expertes" in name:
        return "math_expertes"
    if "complementaires" in name:
        return "math_complementaires"
    if "specialite" in name:
        return "specialite_math"
    return "standard"


# ***** CORE *****

def normalize_filename(name: str) -> str:
    clean_name = clean_text(name)

    # ***** LEVEL *****
    if "seconde" in clean_name:
        level = "seconde"
    elif "premiere" in clean_name:
        level = "premiere"
    elif "terminale" in clean_name:
        level = "terminale"
    else:
        raise ValueError(f"Level introuvable: {name}")

    # ***** TRACK *****
    if "technologique" in clean_name:
        track = "technologique"
    else:
        track = "generale"

    # ***** TYPE *****
    if "specialite" in clean_name:
        type_ = "specialite"
    elif "complementaires" in clean_name:
        type_ = "complementaires"
    elif "scientifique" in clean_name:
        type_ = "scientifique"
    else:
        type_ = "standard"

    # ***** YEAR *****
    year = extract_year(name)

    return f"BO_lycee_{level}_{track}_{type_}_{year}.pdf"


def process_files():
    for file in RAW_DIR.glob("*.pdf"):
        try:
            new_name = normalize_filename(file.name)
            target_path = PROCESSED_DIR / new_name

            shutil.copy(file, target_path)

            logger.info(f"[PROCESSING] ✔ {file.name} → {new_name}")

        except Exception as e:
            logger.error(f"[PROCESSING] ❌ Error with {file.name}: {e}")


