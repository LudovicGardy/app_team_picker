import pandas as pd
import streamlit as st

from medals.medals import get_medals
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

        # try:
        #     with st.container(border=True):
        #         self.display_medals_JO24()
        # except Exception as e:
        #     print(e)
        #     st.error("Erreur lors de l'affichage des médailles")

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

    @st.experimental_fragment
    def display_medals_JO24(self):
        st.markdown(
            '<div class="main-title">Tableau des médailles JO 2024</div>',
            unsafe_allow_html=True,
        )

        medals_france = get_medals("France")
        medals_usa = get_medals("USA")
        medals_japan = get_medals("Chine")

        data = {
            "Pays": ["", "🇫🇷 France", "🇺🇸 USA", "🇨🇳 Chine"],
            "Or": [
                "🥇",
                medals_france["gold_medals"],
                medals_usa["gold_medals"],
                medals_japan["gold_medals"],
            ],
            "Argent": [
                "🥈",
                medals_france["silver_medals"],
                medals_usa["silver_medals"],
                medals_japan["silver_medals"],
            ],
            "Bronze": [
                "🥉",
                medals_france["bronze_medals"],
                medals_usa["bronze_medals"],
                medals_japan["bronze_medals"],
            ],
            "Total": [
                "🥇🥈🥉",
                medals_france["total_medals"],
                medals_usa["total_medals"],
                medals_japan["total_medals"],
            ],
        }

        df = pd.DataFrame(data)

        # st.table(df.style.hide(axis='index'))
        st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    app = App()
