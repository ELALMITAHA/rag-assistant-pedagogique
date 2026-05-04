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
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&#039;", "'")
    return text.strip()

def extract_date(text):
    match = re.search(r"(\d{1,2}) ([a-zéû]+) (\d{4})", text.lower())
    if match:
        day, month, year = match.groups()
        month = MONTHS.get(month, "01")
        return f"{year}-{month}-{int(day):02d}"
    return "unknown"

def scrape_programmes():
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





