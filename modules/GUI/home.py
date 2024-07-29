import random
import time
from datetime import datetime

import streamlit as st

from modules.utils import load_phrases, normalize_value


class Home:
    def __init__(self, team_name: str):
        assert isinstance(team_name, str), "team_name must be a string"
        assert team_name.strip(), "team_name must not be empty"

        self.team_name = team_name

        tabs = st.tabs(
            [
                "🎲 Sélectionner un candidat",
                "🚸 Ajouter / Supprimer un membre",
                "🔴 Signaler un blocage / une update",
            ]
        )

        self.display_members_alerts()
        self.display_members()

        with tabs[0]:
            self.display_home_tab()
            self.display_logs()

        with tabs[1]:
            self.display_add_remove_tab()

        with tabs[2]:
            self.display_blocage_tab()

    def display_members(self):
        try:
            self.database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        members = self.database.load_members(self.team_name)

        self.active_members = []
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
                    self.active_members.append(member["name"])
                self.database.save_member(self.team_name, member)

                progress_bar.progress(
                    normalize_value(i + 1, 0, len(members)), text=progress_text
                )
            progress_bar.empty()

    def display_members_alerts(self):
        members_alerts = {"blocage": [], "update": []}

        try:
            self.database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        members = self.database.load_members(self.team_name)

        for member in members:
            with st.sidebar:
                try:
                    if member["active"] and member["is_blocked"]:
                        members_alerts["blocage"].append(member["name"])
                except:
                    pass

                try:
                    if member["active"] and member["is_update"]:
                        members_alerts["update"].append(member["name"])
                except:
                    pass

        if members_alerts["blocage"]:
            for member in members_alerts["blocage"]:
                st.sidebar.warning(f"⚠️ {member}")

        if members_alerts["update"]:
            for member in members_alerts["update"]:
                st.sidebar.success(f"❇️ {member}")

        if not members_alerts["blocage"] and not members_alerts["update"]:
            st.sidebar.info("Aucun blocage ou update signalé")

        st.sidebar.divider()

    def display_home_tab(self):
        try:
            wrap_phrases = load_phrases("config/wrap_phrases.yaml")
        except FileNotFoundError:
            raise FileNotFoundError("wrap_phrases.yaml file not found")

        with st.container(border=True):
            st.markdown(
                '<div class="header">A l\'ordre du jour...</div>',
                unsafe_allow_html=True,
            )

            if st.button("**▶ DESIGNER UN MEMBRE**"):
                if self.active_members:
                    selected_person = random.choice(self.active_members)
                    phrase = random.choice(wrap_phrases).split("{}")
                    self.database.log_result(self.team_name, selected_person)

                    with st.status("Chargement...", expanded=True) as status:
                        st.write("Recherche d'un candidat...")
                        time.sleep(2)
                        st.write("Validation du candidat...")
                        time.sleep(1)
                        st.write("Candidat trouvé !")
                        time.sleep(2)
                        status.update(
                            label="Candidat trouvé !", state="complete", expanded=False
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

    def display_logs(self):
        with st.expander("🗃️ Consulter l'historique"):
            logs = self.database.load_logs(self.team_name)
            if logs:
                for log in logs:
                    log = f"{log['name']} - {log['timestamp']}"
                    name, timestamp = log.split(" - ")
                    timestamp = datetime.fromisoformat(timestamp)

                    formatted_timestamp = timestamp.strftime("%d %B %Y, %H:%M:%S")
                    readable_log = f"{formatted_timestamp}: {name}"
                    st.write(f"- {readable_log}")
            else:
                st.write("Aucun historique disponible")

    def display_add_remove_tab(self):
        try:
            database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        st.markdown(
            '<div class="header"> Ajouter un membre à la base de données</div>',
            unsafe_allow_html=True,
        )

        new_member = st.text_input(" ")
        if st.button("❎ Ajouter", key="add_member"):
            member = {"name": new_member.capitalize(), "active": True}
            database.save_member(self.team_name, member)
            st.rerun()

        st.divider()

        members = database.load_members(self.team_name)
        members_names = [member["name"] for member in members]
        st.markdown(
            '<div class="header">Supprimer un membre de la base de données</div>',
            unsafe_allow_html=True,
        )
        member_to_remove = st.selectbox(" ", members_names)
        if st.button("❌ Supprimer", key="remove_member"):
            database.delete_member(self.team_name, member_to_remove)
            st.rerun()

    def display_blocage_tab(self):
        try:
            database = st.session_state["database"]
        except KeyError:
            raise KeyError("database object not found in session state")

        st.markdown(
            '<div class="header">Signaler un blocage ou une update</div>',
            unsafe_allow_html=True,
        )

        members = database.load_members(self.team_name)
        members_names = [member["name"] for member in members]

        selected_member = st.selectbox("", members_names)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⚠️ Signaler un blocage"):
                member = next(
                    (m for m in members if m["name"] == selected_member), None
                )
                if member:
                    member["is_blocked"] = True
                    database.save_member(self.team_name, member)
                    st.markdown(
                        f'<div class="success">{selected_member} a signalé un blocage.</div>',
                        unsafe_allow_html=True,
                    )
                    st.rerun()

        with col2:
            if st.button("🆕 Signaler une update"):
                member = next(
                    (m for m in members if m["name"] == selected_member), None
                )
                if member:
                    member["is_update"] = True
                    database.save_member(self.team_name, member)
                    st.markdown(
                        f'<div class="success">{selected_member} a signalé une update.</div>',
                        unsafe_allow_html=True,
                    )
                    st.rerun()

        with col3:
            if st.button("🗑️ Réinitialiser mes alertes"):
                member = next(
                    (m for m in members if m["name"] == selected_member), None
                )
                if member:
                    member["is_blocked"] = False
                    member["is_update"] = False
                    database.save_member(self.team_name, member)
                    st.markdown(
                        f'<div class="success">{selected_member} a été réinitialisé.</div>',
                        unsafe_allow_html=True,
                    )
                    st.rerun()
