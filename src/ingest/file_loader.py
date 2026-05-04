import os 
import sys
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader 

from config.path_config import DATA_DIR,PROCESSED_DIR 
from config.settings  import PAGE_URL

from utils.logger import logger

def get_metadata_from_file_name(file_name: str):

    parts = file_name.replace(".pdf", "").split("_")

    return {
        "niveau": parts[1] if len(parts) > 1 else "unknown",
        "classe": parts[2] if len(parts) > 2 else "unknown",
        "voie": parts[3] if len(parts) > 3 else "unknown",
        "filiere": parts[4] if len(parts) > 4 else "unknown",
        "annee": parts[-1] if parts[-1].isdigit() else "unknown"
    }

def load_pdfs(path_to_files): 

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
        try :
            loader = PyMuPDFLoader(str(file_path))
            docs = loader.load()
    
            file_name = str(file_path.relative_to(PROCESSED_DIR))
            file_meta = get_metadata_from_file_name(file_name)
            
            url = PAGE_URL

            global_meta = {
                **file_meta,
                "source": url,
                "file_name": file_name,
                "title": file_name.replace(".pdf", "")
            }
            # 🔥 2. propagation à toutes les pages
            for d in docs:

                d.metadata = {
                    **d.metadata,   # garde page + infos loader
                    **global_meta   # ajoute metadata PDF
                }
            logger.info(f"Metadata ajoutée au fichier {file_name} avec succée !")
            all_docs.extend(docs)
        except Exception as e:
            logger.warning(
                f"Fichier ignoré (ingestion RAG échouée) : {file_name} | Erreur : {str(e)}"
            )

    return all_docs 


    

