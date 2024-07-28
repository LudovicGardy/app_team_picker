import uuid
from datetime import datetime
from typing import Callable

import firebase_admin
from firebase_admin import credentials, firestore

from modules.config import firebase_credentials


class Database:
    def __init__(self):
        self.app_uuid = str(uuid.uuid4())
        self.initialize_firebase(firebase_credentials)

    def initialize_firebase(self, credentials_func: Callable):
        try:
            cred = credentials_func()
            cred = credentials.Certificate(cred)
            app = firebase_admin.initialize_app(cred, name=self.app_uuid)
            self.db = firestore.client(app=app)
        except Exception as e:
            raise RuntimeError(f"Error initializing Firebase: {e}")

    def ensure_initialized(self):
        if not hasattr(self, "db") or self.db is None:
            raise RuntimeError(
                "Firebase database is not initialized. Call initialize_firebase() first."
            )

    def get_team_collection(self, team_name: str) -> firestore.CollectionReference:
        return self.db.collection("teams").document(team_name).collection("members")

    def get_log_collection(self, team_name: str) -> firestore.CollectionReference:
        return self.db.collection("teams").document(team_name).collection("logs")

    def load_members(self, team_name: str) -> list[dict]:
        self.ensure_initialized()
        members_ref = self.get_team_collection(team_name)
        members = []
        docs = members_ref.stream()
        for doc in docs:
            members.append(doc.to_dict())
        return members

    def save_member(self, team_name: str, member: dict):
        self.ensure_initialized()
        member_ref = self.get_team_collection(team_name).document(member["name"])
        member_ref.set(member)

    def delete_member(self, team_name: str, member_name: str):
        self.ensure_initialized()
        member_ref = self.get_team_collection(team_name).document(member_name)
        member_ref.delete()

    def log_result(self, team_name: str, name: str):
        self.ensure_initialized()
        log_ref = self.get_log_collection(team_name).document()
        log_ref.set({"name": name, "timestamp": datetime.now()})

    def load_logs(self, team_name: str) -> list[dict]:
        self.ensure_initialized()
        logs_ref = self.get_log_collection(team_name)
        logs = []
        docs = logs_ref.stream()
        for doc in docs:
            logs.append(doc.to_dict())
        return logs
