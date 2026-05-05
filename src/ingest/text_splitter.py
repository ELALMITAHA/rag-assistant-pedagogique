from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from utils.logger import logger

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(all_docs):
    """
        Découpe une liste de documents en chunks pour un usage en Retrieval-Augmented Generation (RAG).

        Parameters
        ----------
        all_docs : list
            Liste de documents chargés (format LangChain Document),
            généralement issus du chargement de fichiers PDF.

        Behavior
        --------
        - Vérifie que la liste de documents n’est pas vide.
        - Initialise un text splitter de type RecursiveCharacterTextSplitter.
        - Découpe les documents en chunks de taille définie.
        - Gère un overlap entre chunks pour préserver le contexte.
        - Utilise une hiérarchie de séparateurs pour une découpe intelligente :
        paragraphes, lignes, phrases, mots.
        - Log le nombre de documents et de chunks générés.

        Returns
        -------
        list
            Liste de chunks de texte (LangChain Document).

        Raises
        ------
        ValueError
            Si la liste de documents d’entrée est vide.

        Notes
        -----
        - Étape critique pour la qualité du retrieval en RAG.
        - Le choix des paramètres de chunking influence directement la pertinence
        des réponses du modèle.
    """

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
    logger.info(f"{len(all_docs)} pages découpés en {len(chunks)} Chunks avec succé !")

    return chunks

