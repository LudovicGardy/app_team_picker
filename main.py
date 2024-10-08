import pandas as pd
import streamlit as st

from modules.config import check_password, page_config
from modules.GUI.home import Home
from modules.GUI.ui_components import (
    display_sidebar,
    init_page_config,
    init_session_state,
    load_css,
)


class App:
    def __init__(self):
        init_session_state()
        init_page_config(page_config)

        try:
            load_css("config/styles.css")
        except FileNotFoundError:
            raise FileNotFoundError("styles.css file not found")

        st.markdown(
            '<div class="main-title"><h1>Réunion de la Table Ovale</h1></div>',
            unsafe_allow_html=True,
        )

        with st.sidebar:
            display_sidebar(page_config)

        pg = st.navigation(
            [
                st.Page(self.accueil, title="Accueil", icon="🏠"),
                st.Page(self.maite, title="MAITE", icon="🌾"),
            ]
        )
        pg.run()

    def accueil(self):
        team_name = st.sidebar.selectbox("Sélectionner une équipe", ["team_test"])

        home = Home(str(team_name))

    def maite(self):
        if not check_password(st):
            st.stop()

        team_name = st.sidebar.selectbox(
            "Sélectionner une équipe", ["team_build", "team_deploy"]
        )

        home = Home(str(team_name))

if __name__ == "__main__":
    app = App()
