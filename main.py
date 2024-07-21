import streamlit as st
from modules.config import page_config, check_password
from modules.ui_components import init_page_config, load_css, display_sidebar, display_home_tab, display_add_remove_tab, init_session_state
import hmac

class App:
    def __init__(self):

        init_session_state()
        init_page_config(page_config)
        load_css('config/styles.css')
        
        st.markdown('<div class="main-title">Réunion de la Table Ovale</div>', unsafe_allow_html=True)

        with st.sidebar:
            display_sidebar(page_config)

        pg = st.navigation([
            st.Page(self.accueil, title="Accueil", icon="🏠"),
            st.Page(self.maite, title="MAITE", icon="🌾"),
        ])
        pg.run()

    def accueil(self):

        team_name = st.sidebar.selectbox("Sélectionner une équipe", ["team_test"])

        tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

        with tabs[0]:
            display_home_tab(team_name)

        with tabs[1]:
            display_add_remove_tab(team_name)

    def maite(self):

        if not check_password(st):
            st.stop()

        team_name = st.sidebar.selectbox("Sélectionner une équipe", ["team_build", "team_deploy"])

        tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

        with tabs[0]:
            display_home_tab(team_name)

        with tabs[1]:
            display_add_remove_tab(team_name)

    
if __name__ == '__main__':
    app = App()



