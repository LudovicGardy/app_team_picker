import yaml

def load_phrases(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        phrases = yaml.safe_load(file)
    return phrases['wrap_phrases']

def normalize_value(value, old_min=0, old_max=12):
    ### Normalize the value between 0 and 1
    normalized_value = (value - old_min) / (old_max - old_min)
    return normalized_value