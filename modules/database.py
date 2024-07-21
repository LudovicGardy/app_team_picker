import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime
from modules.config import firebase_credentials
import streamlit as st
from datetime import datetime

class Database:

    def __init__(self):
        self.initialize_firebase(firebase_credentials)

    def initialize_firebase(self, credentials_func):
        if 'database' not in st.session_state:
            if not firebase_admin._apps:
                try:
                    cred = credentials_func()
                    cred = credentials.Certificate(cred)
                    app = firebase_admin.initialize_app(cred)#, name=datetime.now().strftime('%Y%m%d%H%M%S'))
                    st.session_state['database'] = firestore.client(app=app)
                except Exception as e:
                    print(f"Erreur lors de l'initialisation de Firebase: {e}")
        self.db = st.session_state['database']

    def ensure_initialized(self):
        if not hasattr(self, 'db') or self.db is None:
            raise RuntimeError("Firebase database is not initialized. Call initialize_firebase() first.")

    def load_members(self, team_name):
        self.ensure_initialized()
        members_ref = self.db.collection('teams').document(team_name).collection('members')
        members = []
        docs = members_ref.stream()
        for doc in docs:
            members.append(doc.to_dict())
        return members

    def save_member(self, team_name, member):
        self.ensure_initialized()
        member_ref = self.db.collection('teams').document(team_name).collection('members').document(member['name'])
        member_ref.set(member)

    def delete_member(self, team_name, member_name):
        self.ensure_initialized()
        member_ref = self.db.collection('teams').document(team_name).collection('members').document(member_name)
        member_ref.delete()

    def log_result(self, team_name, name):  
        self.ensure_initialized()
        log_ref = self.db.collection('teams').document(team_name).collection('logs').document()
        log_ref.set({'name': name, 'timestamp': datetime.now()})
