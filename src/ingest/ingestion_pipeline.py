from config.path_config import PROCESSED_DIR 
from utils.logger import logger

from src.ingest.bo_downaloader import scrape_programmes,download_programmes
from src.ingest.normalize_filenames import process_files
from src.ingest.file_loader import load_pdfs
from src.ingest.text_splitter import split_documents
from src.ingest.vectore_store import vector_store

from langchain_mistralai import MistralAIEmbeddings

from dotenv import load_dotenv
import os

def ingestion_pipeline():
    """
        Exécute le pipeline complet d’ingestion des programmes de mathématiques
        dans une base vectorielle pour un système RAG.

        Behavior
        --------
        Ce pipeline enchaîne les étapes suivantes :

        1. Scraping des programmes officiels depuis une source web.
        2. Téléchargement des fichiers PDF associés.
        3. Normalisation des noms de fichiers pour homogénéiser les données.
        4. Chargement des PDF et enrichissement des métadonnées.
        5. Découpage des documents en chunks exploitables pour le retrieval.
        6. Génération des embeddings via un modèle MistralAI.
        7. Stockage des embeddings dans une base vectorielle.

        Notes
        -----
        - Pipeline conçu pour être exécuté de manière batch.
        - Idempotent si les fichiers existent déjà côté stockage local.
        - Dépend de services externes (API embeddings MistralAI).
        - Utilisé comme étape initiale du système RAG.

        Returns
        -------
        None
            La fonction ne retourne rien, elle construit uniquement les artefacts
            nécessaires au système de retrieval.
    """
    
    logger.info("================= Starting data ingestion pipeline ====================")
    # ==================================
    # DOWNLOAD PROGRAMS AS PDFS FILES
    # ==================================
    programmes = scrape_programmes()
    download_programmes(programmes)

    # ===================================
    # PROCESS FILES NAMES 
    # ===================================
    process_files()
    
    # ===================================
    # Load PDFs and add metadata 
    # ===================================
    all_docs = load_pdfs(PROCESSED_DIR)

    # ===================================
    # Split text to chunks 
    # ===================================
    chunks = split_documents(all_docs)

    load_dotenv()
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    vector_store(chunks,embeddings)
