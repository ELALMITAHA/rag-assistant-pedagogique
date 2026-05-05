# 📘 RAG Assistant Pédagogique — Mathématiques (France 🇫🇷)

> Un assistant intelligent basé sur un système **RAG (Retrieval-Augmented Generation)** permettant d’interroger les programmes officiels de mathématiques du lycée français.

---

## 🚀 Pourquoi ce projet ?

Les programmes officiels de mathématiques sont :
- longs
- fragmentés
- difficiles à naviguer

👉 Ce projet transforme ces documents en **assistant conversationnel intelligent**, capable de répondre directement à des questions pédagogiques précises.

---

## 🧠 Ce que fait le système

L’utilisateur pose une question en langage naturel :

> *“Quelles sont les notions de probabilités en terminale ?”*

Et le système :

✔ comprend la question  
✔ recherche les passages pertinents dans les programmes officiels  
✔ filtre selon le niveau scolaire  
✔ rerank les résultats  
✔ génère une réponse claire et structurée  

---

## ⚙️ Architecture du pipeline RAG


User Query
↓
Query Rewriting (LLM)
↓
Embedding (Mistral AI)
↓
Vector Search (Qdrant)
↓
Filtering (classe / voie / filière / année)
↓
Reranking (Cross-Encoder / LLM)
↓
Context Construction
↓
LLM Response Generation
↓
Final Answer + Sources


---

## 🧱 Features principales

### 🔍 Retrieval intelligent
- Recherche vectorielle avec Qdrant
- Filtrage metadata (classe, filière, voie, année)

### 🧠 Intelligence augmentée
- Query rewriting (amélioration automatique des questions)
- Reranking des documents pour meilleure pertinence

### 📚 Données officielles
- Programmes du **Bulletin Officiel de l’Éducation nationale**
- Lycée général et technologique

### ⚡ Pipeline complet
- ingestion → preprocessing → chunking → vectorisation → retrieval → génération

---

## 🛠️ Stack technique

- Python 3.10+
- LangChain
- Qdrant (vector database)
- Mistral AI (LLM + embeddings)
- Streamlit (interface utilisateur)
- PyMuPDF (PDF parsing)
- BeautifulSoup (scraping)

---

## 📁 Architecture du projet


app/
├── main.py
└── app_utils.py

src/
├── ingest/
│ ├── scraping
│ ├── preprocessing
│ ├── ingestion_pipeline.py
│ ├── text_splitter.py
│ └── vector_store.py
│
└── retrieve/
├── query_rewriting.py
├── querying_vector_db.py
├── reranking_documents.py
└── retrieve_pipeline.py

config/
├── prompts
├── settings
└── paths

utils/
└── logger.py

data/
├── raw/
└── processed/


---

## 🚀 Installation & exécution

### 1. Cloner le projet
```bash
git clone <repo_url>
cd rag-assistant
2. Installer les dépendances
pip install -r requirements.txt
3. Variables d’environnement

Créer un fichier .env :

QDRANT_URL=...
QDRANT_API_KEY=...
MISTRAL_API_KEY=...
4. Lancer l’ingestion
python -m src.ingest.ingestion_pipeline
5. Lancer l’application
streamlit run app/main.py