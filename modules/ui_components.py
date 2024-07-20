import streamlit as st
import random
import time
from modules.database import load_members, save_member, delete_member, log_result
from modules.utils import load_phrases

wrap_phrases = load_phrases('config/wrap_phrases.yaml')

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_sidebar(config):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(str(config().get('page_logo')), width=60)
    with col2:
        st.write('# Daily Loto')

    st.caption(str(config().get('page_description')))
    st.divider()

def display_home_tab(team_name):
    st.markdown('<div class="header">Désigner une Personne</div>', unsafe_allow_html=True)
    
    members = load_members(team_name)
    
    active_members = []
    for member in members:
        is_active = st.sidebar.toggle(member['name'], value=member['active'], key=member['name'] + team_name)
        member['active'] = is_active
        if is_active:
            active_members.append(member['name'])
        save_member(team_name, member)
    
    if st.button(''):
        if active_members:
            selected_person = random.choice(active_members)
            phrase = random.choice(wrap_phrases).format(selected_person)
            log_result(team_name, selected_person)
    
            with st.spinner('Tirage en cours...'):
                time.sleep(3)
    
            st.write(f"<h1 style='text-align: center; color: #2874A6;'>{phrase}</h1>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error">Aucun membre actif pour le tirage !</div>', unsafe_allow_html=True)

def display_add_remove_tab(team_name):
    st.markdown('<div class="header">Ajouter un Membre</div>', unsafe_allow_html=True)
    
    new_member = st.text_input('Saisir le nom du membre')
    if st.button('Ajouter', key='add_member'):
        member = {'name': new_member, 'active': True}
        save_member(team_name, member)
        st.markdown(f'<div class="success">{new_member} a été ajouté à la liste.</div>', unsafe_allow_html=True)
        st.rerun()
    
    members = load_members(team_name)
    members_names = [member['name'] for member in members]
    st.markdown('<div class="header">Supprimer un Membre</div>', unsafe_allow_html=True)
    member_to_remove = st.selectbox('Sélectionner un membre à supprimer', members_names)
    if st.button('Supprimer', key='remove_member'):
        delete_member(team_name, member_to_remove)
        st.markdown(f'<div class="success">{member_to_remove} a été supprimé de la liste.</div>', unsafe_allow_html=True)
        st.rerun()
