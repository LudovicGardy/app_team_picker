import yaml

def load_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        phrases = yaml.safe_load(file)
    return phrases['wrap_phrases']
