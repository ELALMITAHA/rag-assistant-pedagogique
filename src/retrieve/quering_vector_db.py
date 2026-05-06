import os 
from dotenv import load_dotenv, find_dotenv

from qdrant_client import models
from qdrant_client import QdrantClient

from config.settings import COLLECTION_NAME 


def query_vector_db(query_vector,classe,voie,filiere,annee,limit):
    """
        Interroge une base vectorielle Qdrant avec filtrage metadata + recherche sémantique.

        Parameters
        ----------
        query_vector : list or np.ndarray
            Vecteur d’embedding représentant la requête utilisateur.

        classe : str
            Filtre sur la classe scolaire (ex: seconde, première, terminale).

        voie : str
            Filtre sur la voie scolaire (générale, technologique).

        filiere : str
            Filtre sur la filière (spécialité, générale, etc.).

        annee : str
            Filtre sur l’année du programme.

        limit : int
            Nombre maximum de résultats retournés par la recherche.

        Behavior
        --------
        - Charge les variables d’environnement (Qdrant URL + API key).
        - Initialise un client Qdrant.
        - Crée des index payload sur les champs metadata si absents.
        - Applique un filtre strict sur les métadonnées (classe, voie, filière, année).
        - Effectue une recherche vectorielle sur la collection.
        - Retourne les documents les plus proches du vecteur de requête.

        Returns
        -------
        list
            Résultats de recherche Qdrant contenant les points les plus pertinents.

        Notes
        -----
        - Combine recherche sémantique + filtrage structuré.
        - Permet de réduire fortement le bruit dans le retrieval RAG.
        - Fonction critique pour la précision des réponses du système.
    """

    
    load_dotenv(find_dotenv())

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit, 
        query_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="metadata.classe",
                    match=models.MatchValue(value=classe)
                ),
                models.FieldCondition(
                    key="metadata.voie",
                    match=models.MatchValue(value=voie)
                ),
                models.FieldCondition(
                    key="metadata.filiere",
                    match=models.MatchValue(value=filiere)
                ),
                models.FieldCondition(
                    key="metadata.annee",
                    match=models.MatchValue(value=annee)
                ),
            ]
        ),
    )

    return search_results
