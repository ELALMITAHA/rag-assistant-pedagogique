from dotenv import load_dotenv,find_dotenv
from pathlib import Path
import os

from config.prompt_config import QUERY_PROMPT, REWRITE_QUERY_PROMPT

from langchain_core.documents import Document

from src.retrieve.quering_vector_db import query_vector_db
from src.retrieve.reranking_documents import rerank_documents
from src.retrieve.models import EMBEDDINGS, LLM, RERANKER 

def retrieve(query,classe,voie,filiere,annee,limit):

    # =========================================================
    # 5 - Question rewriting  
    # =========================================================
    chain_query_rewrite = REWRITE_QUERY_PROMPT | LLM
    rewritten_query = chain_query_rewrite.invoke({
        "question": query,
    })
    print(f"Query reecrite : {rewritten_query}")
    # =========================================================
    # 6. EMBEDDING QUERY (MÊME MODÈLE QUE INGESTION)
    # =========================================================
    query_vector = EMBEDDINGS.embed_query(rewritten_query.content)

    # =========================================================
    # 8. SEARCH QDRANT
    # =========================================================
    search_results = query_vector_db(query_vector,classe,voie, filiere,annee,limit)
    docs = [
        Document(
            page_content=hit.payload["page_content"],
            metadata=hit.payload["metadata"]
        )
        for hit in search_results.points
    ]
    # =========================================================
    # 12. RERANKING
    # =========================================================
    reranked_docs = rerank_documents(RERANKER,rewritten_query.content, docs, top_k=5)

    context = "\n\n".join(
    doc.page_content for doc in reranked_docs
    )

    # =========================================================
    # 14. LLM CALL
    # =========================================================
    chain = QUERY_PROMPT | LLM
    response = chain.invoke({
        "context": context,
        "question": rewritten_query.content
    })

    return response.content


if __name__ == '__main__':
    query = "tu peux me dire quels sont les capacités attendues du cours sur la dérivation "
    print(retrieve(query,classe="premiere", voie="generale",filiere = "specialite", annee="2026",limit=20))
    






