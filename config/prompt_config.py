from langchain_core.prompts import ChatPromptTemplate

QUERY_PROMPT = ChatPromptTemplate.from_template("""
	Tu es un assistant chargé d'extraire des informations.

	RÈGLES :
	- utilise uniquement le contexte
	- copie exactement le texte
	- si rien : "je ne sais pas"
	- ne reformule jamais 
	- ne modifie pas les titres ses sections
        
	Contexte :
	{context}

	Question :
	{question}

	Réponse :
""")
REWRITE_QUERY_PROMPT = ChatPromptTemplate.from_template("""
Tu es un expert du Bulletin Officiel (BO) de mathématiques du lycée français.

Ta tâche est de transformer la question d’un utilisateur en une requête optimisée pour une recherche dans un corpus du BO.

Le BO est structuré en sections officielles :
- Contenus
- Capacités attendues
- Démonstrations
- Exemples d’algorithmes
- Approfondissements possibles

Règles :
- Remplace les mots de l’utilisateur par les intitulés officiels du BO
  (ex : "compétences" → "capacités attendues")
- Identifie le chapitre concerné (ex : trigonométrie)
- Ne reformule PAS librement : normalise vers le vocabulaire BO
- Ne rajoute aucune information
- Produit UNE seule requête optimisée pour recherche vectorielle                                             

Question utilisateur :
{question}

Requête BO optimisée :
""")
