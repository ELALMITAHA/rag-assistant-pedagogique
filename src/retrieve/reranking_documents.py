def rerank_documents(reranker,query, docs, top_k):
    """
        Réordonne une liste de documents selon leur pertinence par rapport à une requête utilisateur.

        Parameters
        ----------
        reranker : object
            Modèle de reranking capable de scorer des paires (query, document).
            Exemple : Cross-Encoder ou modèle LLM de scoring.

        query : str
            Requête utilisateur utilisée comme référence pour le ranking.

        docs : list
            Liste de documents candidats (format LangChain Document),
            généralement issus de la phase de retrieval vectoriel.

        top_k : int, optional
            Nombre de documents les plus pertinents à conserver.
            Par défaut : 5.

        Behavior
        --------
        - Vérifie si la liste de documents est vide.
        - Construit des paires (query, contenu du document tronqué).
        - Calcule un score de pertinence pour chaque paire via le reranker.
        - Trie les documents selon leur score décroissant.
        - Sélectionne les top-k documents les plus pertinents.

        Returns
        -------
        list
            Liste des documents rerankés et filtrés selon la pertinence.

        Notes
        -----
        - Étape critique pour améliorer la qualité du retrieval en RAG.
        - Permet de corriger les limites de la recherche vectorielle brute.
        - Le découpage du texte (ici 2000 caractères) influence la qualité du scoring.
    """
    if not docs:
        return []

    pairs = [(query, doc.page_content[:2500]) for doc in docs]

    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked[:top_k]]