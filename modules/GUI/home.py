import random
import time

import streamlit as st

from modules.utils import load_phrases, normalize_value


class Home:
    def __init__(self, team_name: str):
        assert isinstance(team_name, str), "team_name must be a string"
        assert team_name.strip(), "team_name must not be empty"

        self.team_name = team_name

        tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

        with tabs[0]:
            self.display_home_tab()

        with tabs[1]:
            self.display_add_remove_tab()

    def display_home_tab(self):
        try:
            wrap_phrases = load_phrases("config/wrap_phrases.yaml")
        except FileNotFoundError:
            raise FileNotFoundError("wrap_phrases.yaml file not found")

        try:
            database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        st.markdown(
            '<div class="header">A l\'ordre du jour...</div>', unsafe_allow_html=True
        )

        members = database.load_members(self.team_name)

        active_members = []
        with st.sidebar:
            progress_text = "Operation in progress. Please wait."
            progress_bar = st.progress(0, text=progress_text)

            for i, member in enumerate(members):
                is_active = st.sidebar.toggle(
                    member["name"],
                    value=member["active"],
                    key=member["name"] + self.team_name,
                )
                member["active"] = is_active
                if is_active:
                    active_members.append(member["name"])
                database.save_member(self.team_name, member)
                progress_bar.progress(
                    normalize_value(i + 1, 0, len(members)), text=progress_text
                )
            progress_bar.empty()

        if st.button("DESIGNER UN MEMBRE"):
            if active_members:
                selected_person = random.choice(active_members)
                phrase = random.choice(wrap_phrases).split("{}")
                database.log_result(self.team_name, selected_person)

                with st.status("Chargement...", expanded=True) as status:
                    st.write("Recherche d'un candidat...")
                    time.sleep(2)
                    st.write("Validation du candidat...")
                    time.sleep(1)
                    st.write("Candidate trouvé !")
                    time.sleep(2)
                    status.update(
                        label="Candidate trouvé !", state="complete", expanded=False
                    )

                st.divider()

                if time.localtime().tm_mon == 12:
                    st.snow()
                else:
                    st.balloons()

                st.markdown(
                    f"<h4 class='wrap_phrase'>{phrase[0]}<span class='selected_name'>{selected_person}</span>{phrase[1]}</h4>",
                    unsafe_allow_html=True,
                )
                st.divider()
            else:
                st.markdown(
                    '<div class="error">Aucun membre actif pour le tirage !</div>',
                    unsafe_allow_html=True,
                )

    def display_add_remove_tab(self):
        try:
            database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        st.markdown(
            '<div class="header">Ajouter un Membre</div>', unsafe_allow_html=True
        )

        new_member = st.text_input("Saisir le nom du membre")
        if st.button("Ajouter", key="add_member"):
            member = {"name": new_member, "active": True}
            database.save_member(self.team_name, member)
            st.markdown(
                f'<div class="success">{new_member} a été ajouté à la liste.</div>',
                unsafe_allow_html=True,
            )
            st.rerun()

        members = database.load_members(self.team_name)
        members_names = [member["name"] for member in members]
        st.markdown(
            '<div class="header">Supprimer un Membre</div>', unsafe_allow_html=True
        )
        member_to_remove = st.selectbox(
            "Sélectionner un membre à supprimer", members_names
        )
        if st.button("Supprimer", key="remove_member"):
            database.delete_member(self.team_name, member_to_remove)
            st.markdown(
                f'<div class="success">{member_to_remove} a été supprimé de la liste.</div>',
                unsafe_allow_html=True,
            )
            st.rerun()
