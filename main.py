import streamlit as st
import random
import time
from datetime import datetime
import firebase_admin
from firebase_admin import firestore, credentials
from modules.config import firebase_credentials, page_config

if not firebase_admin._apps:
    try:
        cred = firebase_credentials()
        cred = credentials.Certificate(cred)#'app-team-picker-firebase.json')
        firebase_admin.initialize_app(cred)
    except:
        print("No need to initialize the app")

db = firestore.client()

def load_members(team_name):
    members_ref = db.collection('teams').document(team_name).collection('members')
    members = []
    docs = members_ref.stream()
    for doc in docs:
        members.append(doc.to_dict())
    return members

def save_member(team_name, member):
    member_ref = db.collection('teams').document(team_name).collection('members').document(member['name'])
    member_ref.set(member)

def delete_member(team_name, member_name):
    member_ref = db.collection('teams').document(team_name).collection('members').document(member_name)
    member_ref.delete()

def log_result(team_name, name):
    log_ref = db.collection('teams').document(team_name).collection('logs').document()
    log_ref.set({'name': name, 'timestamp': datetime.now()})

# Liste des phrases rigolotes
funny_phrases = [
    "Bravo... {} ! Tu es le héros du jour!",
    "Félicitations, {} ! Tu es le grand gagnant !",
    "Chapeau bas, {} ! Tu as été tiré au sort !",
    "Hourra pour {} ! C’est ton jour de chance !",
    "Youpi, {} ! Tu es notre super star !"
]

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('config/styles.css')

st.markdown('<div class="main-title">Application de Tirage au Sort</div>', unsafe_allow_html=True)

with st.sidebar:

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(str(page_config().get('page_logo')), width=60)
    with col2:
        st.write('# Daily Loto')

    st.caption(str(page_config().get('page_description')))

    st.divider()

team_name = st.sidebar.selectbox("Sélectionner une équipe", ["team_build", "team_deploy", "team_test"])

tabs = st.tabs(["Accueil", "Ajouter/Supprimer un membre"])

with tabs[0]:
    st.markdown('<div class="header">Désigner une Personne</div>', unsafe_allow_html=True)
    
    members = load_members(team_name)
    
    active_members = []
    for member in members:
        is_active = st.sidebar.toggle(member['name'], value=member['active'], key=member['name'] + team_name)
        member['active'] = is_active
        if is_active:
            active_members.append(member['name'])
        save_member(team_name, member)
    
    if st.button('DESIGNER UNE PERSONNE'):
        if active_members:
            selected_person = random.choice(active_members)
            phrase = random.choice(funny_phrases).format(selected_person)
            log_result(team_name, selected_person)
    
            with st.spinner('Tirage en cours...'):
                time.sleep(3)  # Attendre 3 secondes pour l'effet
    
            st.write(f"<h1 style='text-align: center; color: #2874A6;'>{phrase}</h1>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="error">Aucun membre actif pour le tirage !</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown('<div class="header">Ajouter un Membre</div>', unsafe_allow_html=True)
    
    new_member = st.text_input('Saisir le nom du membre')
    if st.button('Ajouter', key='add_member'):
        member = {'name': new_member, 'active': True}
        save_member(team_name, member)
        st.markdown(f'<div class="success">{new_member} a été ajouté à la liste.</div>', unsafe_allow_html=True)
        st.experimental_rerun()
    
    members_names = [member['name'] for member in members]
    st.markdown('<div class="header">Supprimer un Membre</div>', unsafe_allow_html=True)
    member_to_remove = st.selectbox('Sélectionner un membre à supprimer', members_names)
    if st.button('Supprimer', key='remove_member'):
        delete_member(team_name, member_to_remove)
        st.markdown(f'<div class="success">{member_to_remove} a été supprimé de la liste.</div>', unsafe_allow_html=True)
        st.experimental_rerun()
