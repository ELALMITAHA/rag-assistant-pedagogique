import os 
import sys
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader 

from config.path_config import DATA_DIR,PROCESSED_DIR 
from config.settings  import PAGE_URL

from langchain_core.documents import Document

from utils.logger import logger

def get_metadata_from_file_name(file_name: str):
    """
    Extrait des métadonnées structurées à partir du nom d’un fichier PDF.

    Parameters
    ----------
    file_name : str
        Nom du fichier PDF contenant des informations encodées
        (séparées par des underscores).

    Behavior
    --------
    - Supprime l’extension .pdf.
    - Découpe le nom de fichier selon le séparateur "_".
    - Extrait des informations sémantiques si disponibles :
      niveau, classe, voie, filière, année.
    - Fournit une valeur "unknown" si une information est absente.

    Returns
    -------
    dict
        Dictionnaire contenant les métadonnées :
        - niveau : str
        - classe : str
        - voie : str
        - filiere : str
        - annee : str
    """
    parts = file_name.replace(".pdf", "").split("_")

    return {
        "niveau": parts[1] if len(parts) > 1 else "unknown",
        "classe": parts[2] if len(parts) > 2 else "unknown",
        "voie": parts[3] if len(parts) > 3 else "unknown",
        "filiere": parts[4] if len(parts) > 4 else "unknown",
        "annee": parts[-1] if parts[-1].isdigit() else "unknown"
    }


def load_pdfs(path_to_files):
    """
    Charge des fichiers PDF et les transforme en documents exploitables
    pour un pipeline RAG, avec enrichissement des métadonnées.

    Parameters
    ----------
    path_to_files : str or pathlib.Path
        Chemin vers le dossier contenant les fichiers PDF à ingérer.

    Behavior
    --------
    - Vérifie l'existence du dossier d'entrée.
    - Récupère tous les fichiers PDF du dossier.
    - Charge chaque PDF via PyMuPDFLoader.
    - Extrait les métadonnées à partir du nom de fichier.
    - Ajoute des métadonnées globales (source, titre, nom fichier).
    - Injecte ces métadonnées dans chaque page/document.
    - Concatène tous les documents dans une liste finale.
    - Ignore les fichiers en erreur sans bloquer le pipeline global.

    Returns
    -------
    list
        Liste de documents enrichis (format LangChain Document).

    Raises
    ------
    FileNotFoundError
        Si le dossier est introuvable ou vide.

    Notes
    -----
    - Fonction robuste pour ingestion batch en contexte RAG.
    - Tolérante aux erreurs de fichiers individuels.
    - Les métadonnées sont propagées à chaque page pour
      améliorer le retrieval et le reranking.
    """
    path = Path(path_to_files)

    if not path.exists():
        logger.error(f"Le dossier {path} est introuvable")
        raise FileNotFoundError(f"Le Dossier {path} introuvable pour ingestion RAG")
    
    list_of_documents_paths = list(path.glob("*.pdf"))
    
    if not list_of_documents_paths:
        logger.error(f"Le dossier {path} est vide")
        raise FileNotFoundError(f"Le dossier {path} est vide")
  
    all_docs = []

    for file_path in list_of_documents_paths:
        try:
            loader = PyMuPDFLoader(str(file_path))
            pages = loader.load()

            # 🔥 MODIFICATION CLÉ : concaténation du document entier
            full_text = "\n".join([p.page_content for p in pages])

            file_name = str(file_path.relative_to(PROCESSED_DIR))
            file_meta = get_metadata_from_file_name(file_name)

            url = PAGE_URL

            global_meta = {
                **file_meta,
                "source": url,
                "file_name": file_name,
                "title": file_name.replace(".pdf", "")
            }

            # 🔥 UN SEUL Document par PDF (au lieu de 1 par page)
            doc = Document(
                page_content=full_text,
                metadata=global_meta
            )

            logger.info(f"Document reconstruit (full_text) pour {file_name}")

            all_docs.append(doc)

        except Exception as e:
            logger.warning(
                f"Fichier ignoré (ingestion RAG échouée) : {file_path} | Erreur : {str(e)}"
            )

    return all_docs

    

