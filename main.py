import streamlit as st
import random
import time

from modules.config import page_config, firebase_credentials
from modules.database import initialize_firebase, load_members, save_member, delete_member, log_result
from modules.ui_components import load_css, display_sidebar, display_home_tab, display_add_remove_tab

initialize_firebase(firebase_credentials)

load_css('config/styles.css')
st.markdown('<div class="main-title">Réunion de la Table Ovale</div>', unsafe_allow_html=True)

with st.sidebar:
    display_sidebar(page_config)

team_name = st.sidebar.selectbox("Sélectionner une équipe", ["team_build", "team_deploy", "team_test"])

tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

with tabs[0]:
    display_home_tab(team_name)

with tabs[1]:
    display_add_remove_tab(team_name)
