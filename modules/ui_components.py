import streamlit as st
import random
import time
from modules.utils import load_phrases, normalize_value
from modules.database import Database

# if 'database' not in st.session_state:
#     from modules.database import Database
#     st.session_state['database'] = Database()

def init_page_config(page_config): ### Must be called before any other st. function
    st.set_page_config(page_title=page_config().get('page_title'), 
                page_icon = page_config().get('page_icon'),  
                layout = page_config().get('layout'),
                initial_sidebar_state = page_config().get('initial_sidebar_state'))

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

def init_session_state():
    # if 'database' not in st.session_state:
    st.session_state['database'] = Database()

def display_sidebar(page_config):
    logo_path = page_config().get('page_logo')
    desired_width = 60

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(logo_path, width=desired_width)
    with col2:
        st.write(page_config().get('sidebar_title'))

    st.caption(page_config().get('page_description'))
    st.divider()

def display_home_tab(team_name):
    wrap_phrases = load_phrases('config/wrap_phrases.yaml')

    database = st.session_state['database']

    st.markdown('<div class="header">A l\'ordre du jour...</div>', unsafe_allow_html=True)
    
    members = database.load_members(team_name)
    
    active_members = []
    with st.sidebar: ### Spinner is displayed in the sidebar

        progress_text = "Operation in progress. Please wait."
        progress_bar = st.progress(0, text=progress_text)

        for i, member in enumerate(members):
            is_active = st.sidebar.toggle(member['name'], value=member['active'], key=member['name'] + team_name) 
            member['active'] = is_active
            if is_active:
                active_members.append(member['name'])
            database.save_member(team_name, member)
            progress_bar.progress(normalize_value(i+1,0,len(members)), text=progress_text) 
        progress_bar.empty()

    if st.button('DESIGNER UN MEMBRE'):
        if active_members:
            selected_person = random.choice(active_members)
            phrase = random.choice(wrap_phrases).split('{}')
            database.log_result(team_name, selected_person)
    
            # with st.spinner('Tirage en cours...'):
            #     time.sleep(3)
    
            with st.status("Chargement...", expanded=True) as status:
                st.write("Recherche d'un candidat...")
                time.sleep(2)
                st.write("Validation du candidat...")
                time.sleep(1)
                st.write("Candidate trouvé !")
                time.sleep(2)
                status.update(label="Candidate trouvé !", state="complete", expanded=False)

            st.divider()
             
            if time.localtime().tm_mon == 12:
                st.snow()
            else:
                st.balloons()

            st.markdown(
                f"<h3 class='wrap_phrase'>{phrase[0]}<span class='selected_name'>{selected_person}</span>{phrase[1]}</h3>",
                unsafe_allow_html=True
            )
            st.divider()
        else:
            st.markdown('<div class="error">Aucun membre actif pour le tirage !</div>', unsafe_allow_html=True)

def display_add_remove_tab(team_name):
    database = st.session_state['database']

    st.markdown('<div class="header">Ajouter un Membre</div>', unsafe_allow_html=True)
    
    new_member = st.text_input('Saisir le nom du membre')
    if st.button('Ajouter', key='add_member'):
        member = {'name': new_member, 'active': True}
        database.save_member(team_name, member)
        st.markdown(f'<div class="success">{new_member} a été ajouté à la liste.</div>', unsafe_allow_html=True)
        st.rerun()
    
    members = database.load_members(team_name)
    members_names = [member['name'] for member in members]
    st.markdown('<div class="header">Supprimer un Membre</div>', unsafe_allow_html=True)
    member_to_remove = st.selectbox('Sélectionner un membre à supprimer', members_names)
    if st.button('Supprimer', key='remove_member'):
        database.delete_member(team_name, member_to_remove)
        st.markdown(f'<div class="success">{member_to_remove} a été supprimé de la liste.</div>', unsafe_allow_html=True)
        st.rerun()
