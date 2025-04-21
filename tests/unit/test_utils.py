import unittest
from unittest.mock import patch, mock_open
import yaml
from src.utils import load_phrases, normalize_value

class TestUtils(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{"wrap_phrases": ["phrase1", "phrase2"]}')
    @patch("yaml.safe_load", return_value={"wrap_phrases": ["phrase1", "phrase2"]})
    def test_load_phrases(self, mock_yaml_load, mock_file):
        file_path = "dummy_path.yaml"
        expected_phrases = ["phrase1", "phrase2"]
        phrases = load_phrases(file_path)
        mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")
        mock_yaml_load.assert_called_once()
        self.assertEqual(phrases, expected_phrases)

    def test_normalize_value(self):
        self.assertAlmostEqual(normalize_value(6), 0.5)
        self.assertAlmostEqual(normalize_value(0), 0.0)
        self.assertAlmostEqual(normalize_value(12), 1.0)
        self.assertAlmostEqual(normalize_value(3, 0, 6), 0.5)
        self.assertAlmostEqual(normalize_value(6, 0, 6), 1.0)
        self.assertAlmostEqual(normalize_value(0, 0, 6), 0.0)


if __name__ == "__main__":
    unittest.main()