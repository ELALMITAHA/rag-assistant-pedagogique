from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from dotenv import load_dotenv
import os

from config.settings import COLLECTION_NAME
from utils.logger import logger


def vector_store(chunks, embeddings):

    # =============================
    # Load env
    # =============================
    load_dotenv()

    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    # =============================
    # Qdrant client (direct)
    # =============================
    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )

    # =============================
    # Reset collection
    # =============================
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "size": 1024,
            "distance": "Cosine",
        },
    )

    logger.info("🧹 Collection recréée")

    # =============================
    # Indexation (IMPORTANT FIX)
    # =============================
    vector_store = Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=qdrant_url,          
        api_key=qdrant_api_key, 
        collection_name=COLLECTION_NAME,
    )

    logger.info("🚀 Indexation terminée")

    return vector_store