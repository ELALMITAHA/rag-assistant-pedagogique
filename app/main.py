import sys
from pathlib import Path

import streamlit as st 

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app_utils import add_multiselect_lists

from src.retrieve.retrieve_pipeline import retrieve

# ************************************************************
# ******************** PAGE CONFIGURATION ********************
# ************************************************************

# Configure the Streamlit page (layout, title, sidebar behavior)
st.set_page_config(
    page_title="Assistant Pédagogique",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ************************************************************
# ************************ PAGE TITLE ********************
# ************************************************************
st.title("📚 Assistant Pédagogique BO — Réponses issues du BO")

# Multiselect
classe, voie, filiere = add_multiselect_lists()

#  
_,col,_ = st.columns((1,4,1))


import os
st.write("QDRANT_URL:", os.getenv("QDRANT_URL"))
st.write("QDRANT_API_KEY:", "OK" if os.getenv("QDRANT_API_KEY") else "MISSING")


with col:
    # une idée d'un petit text ici du style Poser une question sur le BO
    query = st.text_input(
        label="",
        placeholder="Saisir votre question"
    )

    search_clicked = st.button("🔎 Rechercher")

    if search_clicked:
        
        #  Vérification query
        if not query.strip():
            st.warning("Veuillez saisir une question.")
            st.stop()
        
        #  Vérification filtres
        missing_fields = []

        if not classe:
            missing_fields.append("classe")
        if not voie:
            missing_fields.append("voie")
        if not filiere:
            missing_fields.append("filière")

        if missing_fields:
            st.warning(
                "Veuillez sélectionner : " + ", ".join(missing_fields) + "."
            )
            st.stop()

        with st.spinner("⏳ Requête en cours... (limite API possible)"):
            try:
                results = retrieve(
                query,
                classe=classe,
                voie=voie,
                filiere=filiere,
                annee="2026",
                limit=10
                )
                st.markdown(results["answer"])

                with st.expander("📄 Voir les sources"):
                    for doc in results["sources"]:
                        meta = doc.metadata

                        st.markdown(
                            f"- [{meta.get('title', 'Document')}]({meta.get('source', '#')}) "
                            f"(page {meta.get('page', '?')})"
                        )

            except Exception as e:
                st.error(f"Erreur : {str(e)}")
                st.exception(e)


