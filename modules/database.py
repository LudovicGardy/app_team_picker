import firebase_admin
from firebase_admin import firestore, credentials
from datetime import datetime

db = None

def initialize_firebase(credentials_func):
    global db
    if not firebase_admin._apps:
        try:
            cred = credentials_func()
            cred = credentials.Certificate(cred)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
        except Exception as e:
            print(f"Erreur lors de l'initialisation de Firebase: {e}")

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
