from langchain_core.prompts import ChatPromptTemplate

QUERY_PROMPT = ChatPromptTemplate.from_template("""
	Tu es un assistant chargé d'extraire des informations à partir d'un contexte.

	RÈGLES STRICTES :
	- Utilise uniquement le contexte fourni.
	- Copie exactement le texte sans reformulation.
	- Ne modifie jamais les titres ni les sections.
	- Si l'information n'est pas dans le contexte, réponds exactement : "je ne sais pas".
	- N'invente jamais de contenu.
                                                
	- Réponds uniquement avec les informations directement liées à la question.
	- N’ajoute pas d’informations provenant d’autres sections proches.
	- Si une section officielle correspond exactement à la question, utilise uniquement cette section.
	- Ne fais pas de synthèse globale du document.

	FORMAT MATHÉMATIQUE :
	- Utilise uniquement LaTeX compatible Markdown.
	- Obligatoire :
	- $...$ pour les formules inline
	- $$...$$ pour les formules en bloc
	- Interdit :
	- \\( ... \\)
	- \\[ ... \\]
	- Toute expression mathématique doit être entourée de $ ou $$.

	EXEMPLE :
	- cos(2π) doit être écrit $\\cos\\left(\\2\pi\\right)$

	STRUCTURE :
	- Utilise "-" pour les listes si nécessaire.
	- Ne rajoute aucune explication.

	CONTEXTE :
	{context}

	QUESTION :
	{question}

	RÉPONSE :
""")

REWRITE_QUERY_PROMPT = ChatPromptTemplate.from_template("""
Tu es un assistant de recherche dans le Bulletin Officiel (BO) de mathématiques.

Ta tâche est de préparer une requête STRICTEMENT lexicale pour une recherche documentaire.

RÈGLES ABSOLUES :
- Interdiction de transformer ou compléter un concept mathématique.
- Interdiction d’ajouter des mots comme "fonction", "par", "modélisation de" si absents.
- Interdiction de reformulation conceptuelle.
- Interdiction de normalisation mathématique.

RÈGLE PRINCIPALE :
👉 La requête finale doit rester aussi proche que possible de la formulation utilisateur.

AUTORISÉ UNIQUEMENT :
- correction orthographe
- suppression de mots inutiles
- réorganisation grammaticale légère sans changement de sens

EXEMPLES :
- "variation exponentielle capacités" → inchangé ou léger nettoyage
- "quadratique capacités attendues" → inchangé ou léger nettoyage

Question :
{question}

Requête BO optimisée :
""")