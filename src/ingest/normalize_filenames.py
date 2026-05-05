import os
import re
import shutil
from pathlib import Path

from config.path_config import PROCESSED_DIR, RAW_DIR
from utils.logger import logger


# ***** HELPERS *****

import unicodedata

def clean_text(text):
    """
        Nettoie un texte en supprimant les accents et en normalisant la casse.

        Parameters
        ----------
        text : str
            Texte brut à normaliser.

        Behavior
        --------
        - Convertit le texte en minuscules.
        - Supprime les accents (normalisation Unicode NFD).
        - Retire les caractères diacritiques.

        Returns
        -------
        str
            Texte normalisé (sans accents, en minuscules).
    """
    text = text.lower()
    
    # remove accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    
    return text

def extract_year(text):
    """
    Extrait une année au format YYYY depuis une chaîne de caractères.

    Parameters
    ----------
    text : str
        Texte contenant potentiellement une année.

    Behavior
    --------
    - Recherche une année commençant par '20'.
    - Retourne la première correspondance trouvée.

    Returns
    -------
    str
        Année extraite ou "unknown" si non trouvée.
    """
    match = re.search(r"(20\d{2})", text)
    return match.group(1) if match else "unknown"

def detect_niveau(name):
    """
    Détecte le niveau scolaire à partir du nom de fichier.

    Parameters
    ----------
    name : str
        Nom du fichier ou texte source.

    Behavior
    --------
    - Identifie si le document appartient au collège ou lycée.
    - Basé sur la présence du mot 'cycle'.

    Returns
    -------
    str
        "college" ou "lycee".
    """
    if "cycle" in name:
        return "college"
    return "lycee"

def detect_classe(name):
    """
    Détecte la classe scolaire à partir du nom de fichier.

    Parameters
    ----------
    name : str
        Nom du fichier à analyser.

    Behavior
    --------
    - Normalise le texte.
    - Identifie la classe (seconde, première, terminale).
    - Gère aussi les cycles collège.
    - Retourne "unknown" si aucune correspondance.

    Returns
    -------
    str
        Classe détectée ou "unknown".
    """
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

def detect_filiere(name):
    """
    Détecte la filière scolaire à partir du nom de fichier.

    Parameters
    ----------
    name : str
        Nom du fichier.

    Behavior
    --------
    - Analyse les mots-clés du programme.
    - Identifie la filière : générale, technologique ou mixte.

    Returns
    -------
    str
        Filière détectée ou "unknown".
    """
    name = clean_text(name)

    if "generale et technologique" in name:
        return "generale_technologique"
    if "technologique" in name:
        return "technologique"
    if "generale" in name:
        return "generale"

    return "unknown"


def detect_option(name):
    """
    Détecte l’option mathématique associée au programme.

    Parameters
    ----------
    name : str
        Nom du fichier à analyser.

    Behavior
    --------
    - Identifie les options : spécialité, complémentaires, expertes.
    - Retourne "standard" si aucune option spécifique.

    Returns
    -------
    str
        Option mathématique détectée.
    """
    if "expertes" in name:
        return "math_expertes"
    if "complementaires" in name:
        return "math_complementaires"
    if "specialite" in name:
        return "specialite_math"
    return "standard"


# ***** CORE *****

def normalize_filename(name):
    """
    Normalise un nom de fichier PDF en un format structuré standardisé.

    Parameters
    ----------
    name : str
        Nom brut du fichier PDF.

    Behavior
    --------
    - Nettoie le texte.
    - Détecte le niveau scolaire (seconde, première, terminale).
    - Détecte la filière (générale ou technologique).
    - Détecte le type de programme (spécialité, complémentaire, standard).
    - Extrait l’année du document.
    - Construit un nom de fichier standardisé pour ingestion RAG.

    Returns
    -------
    str
        Nom de fichier normalisé au format :
        BO_lycee_{level}_{track}_{type}_{year}.pdf

    Raises
    ------
    ValueError
        Si le niveau scolaire ne peut pas être détecté.
    """
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
    """
    Traite les fichiers PDF bruts et les prépare pour le pipeline RAG.

    Behavior
    --------
    - Parcourt tous les fichiers PDF du dossier RAW_DIR.
    - Normalise les noms de fichiers via normalize_filename().
    - Copie les fichiers dans PROCESSED_DIR.
    - Journalise les opérations de transformation.
    - Continue le traitement même en cas d’erreur sur un fichier.

    Notes
    -----
    - Fonction batch utilisée dans le pipeline d’ingestion.
    - Étape de préparation essentielle avant parsing des documents.

    Returns
    -------
    None
        La fonction ne retourne rien, elle prépare uniquement les données.
    """
    for file in RAW_DIR.glob("*.pdf"):
        try:
            new_name = normalize_filename(file.name)
            target_path = PROCESSED_DIR / new_name

            shutil.copy(file, target_path)

            logger.info(f"[PROCESSING] ✔ {file.name} → {new_name}")

        except Exception as e:
            logger.error(f"[PROCESSING] ❌ Error with {file.name}: {e}")


