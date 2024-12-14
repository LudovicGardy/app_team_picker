import unittest
from unittest.mock import patch, MagicMock
import os

import sys
sys.path.append("..")
sys.path.append("../..")

from .modules.config import (
    check_password,
    load_configurations,
    load_toml_config,
    page_config,
    data_URL,
    firebase_credentials,
)


class TestConfig(unittest.TestCase):
    @patch("modules.config.st")
    @patch("modules.config.load_configurations")
    def test_check_password_correct(self, mock_load_configurations, mock_st):
        mock_st.session_state = {"password": "correct_password"}
        mock_load_configurations.return_value = {"PASSWORD": "correct_password"}

        result = check_password(mock_st)
        self.assertTrue(result)
        self.assertTrue(mock_st.session_state["password_correct"])

    @patch("modules.config.st")
    @patch("modules.config.load_configurations")
    def test_check_password_incorrect(self, mock_load_configurations, mock_st):
        mock_st.session_state = {"password": "wrong_password"}
        mock_load_configurations.return_value = {"PASSWORD": "correct_password"}

        result = check_password(mock_st)
        self.assertFalse(result)
        self.assertFalse(mock_st.session_state["password_correct"])

    @patch("modules.config.find_dotenv")
    @patch("modules.config.load_dotenv")
    def test_load_configurations_with_dotenv(self, mock_load_dotenv, mock_find_dotenv):
        mock_find_dotenv.return_value = ".env"
        with patch("builtins.open", unittest.mock.mock_open(read_data="PASSWORD=correct_password")):
            os.environ["PASSWORD"] = "correct_password"
            result = load_configurations()
            self.assertIn("PASSWORD", result)
            self.assertEqual(result["PASSWORD"], "correct_password")

    @patch("modules.config.find_dotenv")
    def test_load_configurations_without_dotenv(self, mock_find_dotenv):
        mock_find_dotenv.return_value = ""
        os.environ["PASSWORD"] = "correct_password"
        result = load_configurations()
        self.assertIn("PASSWORD", result)
        self.assertEqual(result["PASSWORD"], "correct_password")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='[theme]\npage_title = "Test Title"')
    def test_load_toml_config(self, mock_open):
        result = load_toml_config("dummy_path")
        self.assertIn("page_title", result)
        self.assertEqual(result["page_title"], "Test Title")

    def test_load_toml_config_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_toml_config("non_existent_path")

    @patch("modules.config.load_toml_config")
    def test_page_config(self, mock_load_toml_config):
        mock_load_toml_config.return_value = {"page_title": "Test Title"}
        result = page_config()
        self.assertIn("page_title", result)
        self.assertEqual(result["page_title"], "Test Title")

    @patch("modules.config.load_configurations")
    def test_data_URL(self, mock_load_configurations):
        mock_load_configurations.return_value = {
            "AWS_S3_URL": "https://s3.amazonaws.com",
            "DATA_GOUV_URL": "https://data.gouv.fr"
        }
        result = data_URL()
        self.assertIn("summarized_data_url", result)
        self.assertIn("datagouv_source_URL", result)
        self.assertIn("available_years_datagouv", result)
        self.assertIn("scrapped_year_current", result)

    @patch("modules.config.load_configurations")
    def test_firebase_credentials(self, mock_load_configurations):
        mock_load_configurations.return_value = {
            "TYPE": "service_account",
            "PROJECT_ID": "test_project",
            "PRIVATE_KEY_ID": "key_id",
            "PRIVATE_KEY": "private_key/breakline/",
            "CLIENT_EMAIL": "email@test.com",
            "CLIENT_ID": "client_id",
            "AUTH_URI": "https://auth.uri",
            "TOKEN_URI": "https://token.uri",
            "AUTH_PROVIDER_X509_CERT_URL": "https://cert.url",
            "CLIENT_X509_CERT_URL": "https://client.cert.url",
            "UNIVERSE_DOMAIN": "test_domain"
        }
        result = firebase_credentials()
        self.assertIn("type", result)
        self.assertIn("project_id", result)
        self.assertIn("private_key", result)
        self.assertEqual(result["private_key"], "private_key\n")

    @patch("modules.config.load_configurations")
    def test_firebase_credentials_missing_key(self, mock_load_configurations):
        mock_load_configurations.return_value = {
            "TYPE": "service_account",
            "PROJECT_ID": "test_project",
            # Missing PRIVATE_KEY_ID
            "PRIVATE_KEY": "private_key/breakline/",
            "CLIENT_EMAIL": "email@test.com",
            "CLIENT_ID": "client_id",
            "AUTH_URI": "https://auth.uri",
            "TOKEN_URI": "https://token.uri",
            "AUTH_PROVIDER_X509_CERT_URL": "https://cert.url",
            "CLIENT_X509_CERT_URL": "https://client.cert.url",
            "UNIVERSE_DOMAIN": "test_domain"
        }
        with self.assertRaises(ValueError):
            firebase_credentials()


if __name__ == "__main__":
    unittest.main()