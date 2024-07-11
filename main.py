import streamlit as st
import yaml
import random
import time
from datetime import datetime

# Fonction pour charger la configuration
def load_config(file_name):
    with open(f'config/{file_name}', 'r') as file:
        config = yaml.safe_load(file)
    return config

# Fonction pour sauvegarder la configuration
def save_config(file_name, config):
    with open(f'config/{file_name}', 'w') as file:
        yaml.dump(config, file)

# Fonction pour charger les phrases rigolotes
def load_funny_phrases():
    with open('config/funny_phrases.yaml', 'r') as file:
        phrases_config = yaml.safe_load(file)
    return phrases_config['funny_phrases']

# Fonction pour ajouter un membre à la liste
def add_member(file_name, member_name):
    config = load_config(file_name)
    members = config['members']
    if member_name and not any(member['name'] == member_name for member in members):
        members.append({'name': member_name, 'active': True})
        save_config(file_name, config)
        st.experimental_rerun()  # Rafraîchir la page pour afficher le nouveau membre

# Fonction pour supprimer un membre de la liste
def remove_member(file_name, member_name):
    config = load_config(file_name)
    members = config['members']
    members = [member for member in members if member['name'] != member_name]
    config['members'] = members
    save_config(file_name, config)
    st.experimental_rerun()  # Rafraîchir la page pour mettre à jour la liste des membres

# Fonction pour logger l'événement
def log_result(name):
    with open('results_log.txt', 'a') as file:
        file.write(f"{datetime.now()} - {name}\n")

# Charger le CSS depuis un fichier
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Charger le fichier CSS
load_css('config/styles.css')

st.markdown('<div class="main-title">Application de Tirage au Sort</div>', unsafe_allow_html=True)

# Choisir l'équipe
team_choice = st.sidebar.selectbox('Select a team', ['Builders', 'Deployers'])
config_file = 'team_build.yaml' if team_choice == 'Builders' else 'team_deploy.yaml'

st.sidebar.header(f'Current members')

# Créer des onglets
tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

with tabs[0]:
    st.markdown(f'<div class="header">Hello {team_choice}</div>', unsafe_allow_html=True)
    
    config = load_config(config_file)
    members = config['members']
    funny_phrases = load_funny_phrases()
    
    # Ajouter des toggles pour chaque membre
    active_members = []
    for member in members:
        is_active = st.sidebar.toggle(member['name'], value=member['active'], key=member['name'])
        member['active'] = is_active
        if is_active:
            active_members.append(member['name'])
    
    # Sauvegarder l'état des toggles
    save_config(config_file, config)
    
    if st.button('DESIGNER UNE PERSONNE'):
        if active_members:
            selected_person = random.choice(active_members)
            phrase = random.choice(funny_phrases).format(selected_person)
            log_result(selected_person)
    
            with st.spinner('Tirage en cours...'):
                time.sleep(3)  # Attendre 3 secondes pour l'effet
    
            st.write(f"<h1 style='text-align: center; color: #2874A6;'>{phrase}</h1>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error">Aucun membre actif pour le tirage !</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="header">Ajouter/Supprimer un Membre</div>', unsafe_allow_html=True)
    
    new_member = st.text_input('Ajouter un membre')
    if st.button('Ajouter', key='add_member'):
        add_member(config_file, new_member)
        st.markdown(f'<div class="success">{new_member} a été ajouté à la liste.</div>', unsafe_allow_html=True)
    
    members_names = [member['name'] for member in members]
    st.markdown('<div class="header">Supprimer un Membre</div>', unsafe_allow_html=True)
    member_to_remove = st.selectbox('Sélectionner un membre à supprimer', members_names)
    if st.button('Supprimer', key='remove_member'):
        remove_member(config_file, member_to_remove)
        st.markdown(f'<div class="success">{member_to_remove} a été supprimé de la liste.</div>', unsafe_allow_html=True)
