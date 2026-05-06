import os 
import streamlit as st 
from config.path_config import PROCESSED_DIR

#retrieve(query,classe="premiere", voie="generale",filiere = "specialite", annee="2026",limit=10)

def get_multiselect_lists(path_to_pdfs=PROCESSED_DIR):
    list_of_files = os.listdir(path_to_pdfs)

    classes_list = set([c.split("_")[2] for c in list_of_files])
    voies_list =  set([c.split("_")[3] for c in list_of_files])
    filiere_list = set([c.split("_")[4] for c in list_of_files])  

    return classes_list, voies_list, filiere_list

def add_multiselect_lists():
    classes_list, voies_list, filiere_list = get_multiselect_lists()
    
    classe = st.sidebar.selectbox(
        "**Classe**",
        classes_list,
        placeholder="Chosir une classe",
        index=None,
    )
    
    voie = st.sidebar.selectbox(
        "**Voie**",
        voies_list,
        placeholder="Chosir une voie",
        index=None,
    )
    
    filiere_list = st.sidebar.selectbox(
        "**Filière**",
        filiere_list,
        placeholder="Chosir une filière",
        index=None,
    )
    
    return classe, voie, filiere_list


def is_user_choice_valide(classe, voie, filiere, path_to_pdfs=PROCESSED_DIR):

    list_of_files = os.listdir(path_to_pdfs)

    query = f"{classe}_{voie}_{filiere}"

    return any(query in file for file in list_of_files)
    

    
