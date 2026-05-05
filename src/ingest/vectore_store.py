from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from dotenv import load_dotenv
import os

from config.settings import COLLECTION_NAME
from utils.logger import logger


def vector_store(chunks, embeddings):
    """
        Crée et alimente une base vectorielle Qdrant à partir de chunks de documents
        et d’un modèle d’embeddings.

        Parameters
        ----------
        chunks : list
            Liste de documents découpés (chunks) issus du pipeline de preprocessing.
            Chaque chunk contient du texte et des métadonnées associées.

        embeddings : object
            Modèle d’embeddings utilisé pour transformer le texte en vecteurs.
            Exemple : MistralAIEmbeddings.

        Behavior
        --------
        - Charge les variables d’environnement (QDRANT_URL, QDRANT_API_KEY).
        - Initialise un client Qdrant distant.
        - Recrée la collection vectorielle (reset complet des données existantes).
        - Définit la configuration de la collection (dimension + métrique cosine).
        - Indexe les chunks dans la base vectorielle via LangChain Qdrant wrapper.
        - Utilise les embeddings fournis pour vectoriser les documents.
        - Log les étapes critiques du processus d’indexation.

        Returns
        -------
        Qdrant
            Instance de la base vectorielle initialisée et alimentée.

        Notes
        -----
        - Cette fonction écrase systématiquement la collection existante.
        - Étape critique du pipeline RAG (construction de l’index).
        - Dépend d’un service externe (Qdrant Cloud ou instance locale).
    """

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