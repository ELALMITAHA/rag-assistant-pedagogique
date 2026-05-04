import os 
from dotenv import load_dotenv, find_dotenv

from qdrant_client import models
from qdrant_client import QdrantClient

from config.settings import COLLECTION_NAME 


def query_vector_db(query_vector,classe,voie,filiere,annee,limit):

    
    load_dotenv(find_dotenv())

    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME ,
        field_name="metadata.classe",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME ,
        field_name="metadata.voie",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME ,
        field_name="metadata.filiere",
        field_schema="keyword"
    )

    client.create_payload_index(
        collection_name=COLLECTION_NAME ,
        field_name="metadata.annee",
        field_schema="keyword"
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
