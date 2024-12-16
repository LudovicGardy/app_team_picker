import pytest
from unittest.mock import patch, MagicMock
from modules.database import Database
from datetime import datetime

@pytest.fixture
def mock_firebase_credentials():
    with patch("modules.config.firebase_credentials") as mock_creds:
        yield mock_creds

@pytest.fixture
def mock_firestore_client():
    with patch("firebase_admin.firestore.client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_initialize_app():
    with patch("firebase_admin.initialize_app") as mock_init_app:
        yield mock_init_app

@pytest.fixture
def database(mock_firebase_credentials, mock_firestore_client, mock_initialize_app):
    return Database()

def test_ensure_initialized(database):
    database.db = None
    with pytest.raises(RuntimeError, match="Firebase database is not initialized"):
        database.ensure_initialized()

def test_get_team_collection(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    database.get_team_collection(team_name)
    mock_db.collection.assert_called_with("teams")
    mock_db.collection().document.assert_called_with(team_name)
    mock_db.collection().document().collection.assert_called_with("members")

def test_get_log_collection(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    database.get_log_collection(team_name)
    mock_db.collection.assert_called_with("teams")
    mock_db.collection().document.assert_called_with(team_name)
    mock_db.collection().document().collection.assert_called_with("logs")

def test_load_members(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    mock_stream = MagicMock()
    mock_stream.stream.return_value = [MagicMock(to_dict=lambda: {"name": "member1"})]
    mock_db.collection().document().collection().stream = mock_stream.stream
    members = database.load_members(team_name)
    assert members == [{"name": "member1"}]

def test_save_member(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    member = {"name": "member1"}
    database.save_member(team_name, member)
    mock_db.collection().document().collection().document().set.assert_called_with(member)

def test_delete_member(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    member_name = "member1"
    database.delete_member(team_name, member_name)
    mock_db.collection().document().collection().document().delete.assert_called_once()

def test_log_result(database):
    mock_db = MagicMock()
    database.db = mock_db
    team_name = "team1"
    name = "result1"
    database.log_result(team_name, name)
    mock_db.collection().document().collection().document().set.assert_called_once()
