import time
import httpx

from config.prompt_config import QUERY_PROMPT, REWRITE_QUERY_PROMPT

from langchain_core.documents import Document

from src.retrieve.quering_vector_db import query_vector_db
from src.retrieve.reranking_documents import rerank_documents
from src.retrieve.models import EMBEDDINGS, LLM, RERANKER 

from config.settings import LIMIT,TOP_K

def retrieve(query,classe,voie,filiere,annee="2026",limit=LIMIT,top_k=TOP_K):
    """
    Exécute le pipeline complet de retrieval RAG pour répondre à une question utilisateur.

    Parameters
    ----------
    query : str
        Question utilisateur initiale.

    classe : str
        Niveau scolaire (ex: seconde, première, terminale).

    voie : str
        Type de voie scolaire (générale, technologique).

    filiere : str
        Filière ou spécialité associée au programme.

    annee : str, optional
        Année du programme utilisé pour filtrer les documents.
        Par défaut : "2026".

    limit : int, optional
        Nombre maximum de documents récupérés depuis la base vectorielle.

    Behavior
    --------
    Ce pipeline suit les étapes suivantes :

    1. Reformulation de la question utilisateur via un LLM (query rewriting).
    2. Transformation de la requête reformulée en embedding vectoriel.
    3. Recherche sémantique dans la base vectorielle Qdrant avec filtres metadata.
    4. Reconstruction des documents à partir des résultats bruts.
    5. Reranking des documents pour améliorer la pertinence.
    6. Construction du contexte final pour le LLM.
    7. Génération de la réponse finale via un modèle de langage.
    8. Gestion des erreurs API (retry avec backoff exponentiel sur rate limit).

    Returns
    -------
    dict
        Dictionnaire contenant :
        - answer : str
            Réponse générée par le LLM.
        - sources : list
            Documents les plus pertinents utilisés pour générer la réponse.

    Raises
    ------
    Exception
        Si les tentatives de requête échouent après plusieurs retries (rate limit).

    Notes
    -----
    - Pipeline hybride : query rewriting + retrieval vectoriel + reranking + génération.
    - Conçu pour améliorer la précision des réponses sur des documents éducatifs.
    - Intègre une stratégie de robustesse face aux limites API (retry + backoff).
    """

    # =========================================================
    # 1 - Question rewriting  
    # =========================================================
    chain_query_rewrite = REWRITE_QUERY_PROMPT | LLM
    rewritten_query = chain_query_rewrite.invoke({
        "question": query,
    })

    # =========================================================
    # 2. EMBEDDING QUERY (MÊME MODÈLE QUE INGESTION)
    # =========================================================
    query_vector = EMBEDDINGS.embed_query(rewritten_query.content)

    # =========================================================
    # 3. SEARCH QDRANT
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
    # 4. RERANKING
    # =========================================================
    reranked_docs = rerank_documents(RERANKER,rewritten_query.content, docs, top_k=TOP_K)

    # =========================================================
    # 11. DEBUG
    # =========================================================
    # Question de l'utilisateur 
    print("============= User query ======================")
    print(query)

    print("============= Rewrited Query ==================")
    print(rewritten_query.content)

    print("\n===== DOCS FILTRÉS =====\n")

    for d in reranked_docs:
        print(d.metadata.get("title"))
        print(d.metadata.get("classe"), d.metadata.get("voie"))
        print(d.page_content[:200])
        print("------")

        context = "\n\n".join(
        doc.page_content for doc in reranked_docs
        )

    # =========================================================
    # 5. LLM CALL
    # =========================================================
    chain = QUERY_PROMPT | LLM
    for attempt in range(3):
        try:
            response = chain.invoke({
                "context": context,
                "question": rewritten_query.content
            })
            
            return {
            "answer": response.content,
            "sources": reranked_docs[:limit]
            }

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt 
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Rate limit dépassé après plusieurs tentatives.")
  









