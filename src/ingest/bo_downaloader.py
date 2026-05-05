import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from pathlib import Path

from config.settings import (
	BASE_URL,
	PAGE_URL,
	MONTHS
)

from config.path_config import RAW_DIR
from utils.logger import logger

def clean_text(text):
    """
    Nettoie une chaîne de caractères brute extraite du HTML.

    Parameters
    ----------
    text : str
        Texte brut contenant potentiellement des retours à la ligne,
        espaces multiples ou entités HTML.

    Behavior
    --------
    - Remplace les retours à la ligne par des espaces.
    - Normalise les espaces multiples en un seul espace.
    - Remplace les entités HTML courantes (ex: &#039;).
    - Supprime les espaces en début et fin de chaîne.

    Returns
    -------
    str
        Texte nettoyé et normalisé.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&#039;", "'")
    return text.strip()

def extract_date(text):
    """
    Extrait une date au format ISO (YYYY-MM-DD) depuis un texte.

    Parameters
    ----------
    text : str
        Texte contenant une date au format naturel
        (ex: "12 mars 2026").

    Behavior
    --------
    - Recherche une date sous forme "jour mois année".
    - Convertit le mois en numéro via le dictionnaire MONTHS.
    - Construit une date au format ISO.
    - Retourne "unknown" si aucune date n'est trouvée.

    Returns
    -------
    str
        Date au format "YYYY-MM-DD" ou "unknown" si non détectée.
    """
    match = re.search(r"(\d{1,2}) ([a-zéû]+) (\d{4})", text.lower())
    if match:
        day, month, year = match.groups()
        month = MONTHS.get(month, "01")
        return f"{year}-{month}-{int(day):02d}"
    return "unknown"

def scrape_programmes():
    """
    Scrape les programmes officiels de mathématiques depuis une page web.

    Behavior
    --------
    - Effectue une requête HTTP vers la page définie dans PAGE_URL.
    - Parse le HTML avec BeautifulSoup.
    - Recherche la section "Publication des nouveaux programmes".
    - Extrait les liens vers les documents PDF.
    - Construit une structure de données contenant les métadonnées
      (nom, URL, type, date, nom de fichier).

    Returns
    -------
    list of dict
        Liste des programmes extraits avec les champs :
        - name : str
        - url : str
        - type : str
        - date : str
        - filename : str
    """
    response = requests.get(PAGE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # =========================
    # NOUVEAUX PROGRAMMES
    # =========================
    h3_new = soup.find("h3", string=re.compile("Publication des nouveaux programmes", re.I))

    if h3_new:
        links = h3_new.find_next("ul").find_all("a")

        for link in links:
            name = clean_text(link.get_text())
            url = urljoin(BASE_URL, link.get("href"))

            date = "2026-04-02"

            results.append({
                "name": name,
                "url": url,
                "type": "nouveau",
                "date": date,
                "filename": f"{name}_BO {date}.pdf"
            })

    return results

def download_programmes(programmes, raw_dir=RAW_DIR):
    """
    Télécharge une liste de programmes PDF et les stocke localement.

    Parameters
    ----------
    programmes : list of dict
        Liste de dictionnaires représentant les programmes à télécharger.
        Chaque dictionnaire doit contenir au minimum :
        - url : str
        - filename : str

    raw_dir : str or pathlib.Path
        Répertoire de destination pour les fichiers téléchargés.
        Par défaut, utilise RAW_DIR défini dans la configuration.

    Behavior
    --------
    - Crée le dossier cible s'il n'existe pas.
    - Vérifie si le fichier existe déjà pour éviter les doublons.
    - Télécharge chaque fichier via HTTP GET.
    - Sauvegarde les fichiers en binaire.
    - Log les succès et erreurs via le logger.

    Raises
    ------
    requests.RequestException
        En cas d'échec réseau ou réponse HTTP invalide.

    Notes
    -----
    - Le téléchargement est idempotent (skip si fichier déjà présent).
    - Conçu pour un pipeline d'ingestion robuste en contexte MLOps.
    """
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    for p in programmes:
        url = p["url"]
        filename = p["filename"]

        filepath = raw_dir / filename

        # skip si déjà téléchargé
        if filepath.exists():
            print(f"✔️ already exists: {filename}")
            continue

        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(r.content)

            logger.info(f"⬇️ downloaded: {filename}")

        except Exception as e:
            logger.error(f"❌ error {filename} → {e}")





