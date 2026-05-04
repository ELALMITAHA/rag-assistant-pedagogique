from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from utils.logger import logger

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(all_docs):

    if not all_docs:
        logger.error("Aucun doc à découper")
        raise ValueError("Aucun doc à découper")
    
    chunker = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, # à changer  
            chunk_overlap=CHUNK_OVERLAP, # à changer 
            separators=["\n\n","\n","."," ",""]
        )
    # split document prends une liste de l'object documents 
    chunks = chunker.split_documents(documents=all_docs)
    logger.info(f"{len(all_docs)} découpés en {len(chunks)} avec succé !")

    return chunks

