from config.path_config import PROCESSED_DIR 
from utils.logger import logger

from src.scraper import scrape_programmes,download_programmes
from src.normalize_filenames import process_files
from src.loading_files import load_pdfs
from src.text_spliter import split_documents
from src.store_db import vector_store

from langchain_mistralai import MistralAIEmbeddings

from dotenv import load_dotenv
import os

def ingestion_pipeline():
    
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

if __name__ == '__main__':
    ingestion_pipeline()