def rerank_documents(reranker,query, docs, top_k=5):
    if not docs:
        return []

    pairs = [(query, doc.page_content[:2000]) for doc in docs]

    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:top_k]]