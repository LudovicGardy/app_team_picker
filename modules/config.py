import numpy as np
import os
import toml
from dotenv import load_dotenv, find_dotenv
from google.oauth2 import service_account
import hmac

def check_password(st):
    """Returns `True` if the user had the correct password."""

    def password_entered():

        env_variables = load_configurations()
        pw = str(env_variables.get('PASSWORD'))

        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], pw):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

def load_configurations():
    """
    Charge uniquement les variables du fichier .env si celui-ci est présent.
    Si le fichier .env n'existe pas, charge toutes les variables d'environnement du système.
    """
    dotenv_path = find_dotenv('.env')

    if dotenv_path:
        # The .env file exists, load only its variables
        load_dotenv(dotenv_path)
        # Return the variables loaded from the .env
        return {key: os.environ[key] for key in os.environ if key in open(dotenv_path).read()}
    else:
        # The .env file does not exist, return all the system environment variables
        return dict(os.environ)

def load_toml_config(file_path):
    """
    Charge les configurations à partir d'un fichier .toml
    """
    try:
        with open(file_path, 'r') as file:
            return toml.load(file).get('theme', {})
    except FileNotFoundError:
        return {}

def page_config():
    """
    Set the page configuration (title, favicon, layout, etc.)
    """
    env_variables = load_configurations()
    toml_config = load_toml_config('.streamlit/config.toml')

    page_dict = {
        'page_title': toml_config.get('page_title', 'Team Picker'),
        'sidebar_title': f"# {toml_config.get('sidebar_title', 'Team Picker')}",
        'base': toml_config.get('base', 'dark'),
        'page_icon': "images/invivo_DF.png",
        'page_logo': "images/invivo_DF_white.png",
        'layout': toml_config.get('layout', 'centered'),
        'initial_sidebar_state': toml_config.get('initial_sidebar_state', 'auto'),
        'author': 'Sotis AI',
        'markdown': '''
                    <style>
                        .css-10pw50 {
                            visibility:hidden;
                        }
                    </style>
                    ''',
        'page_description': """
            👑 La légende a besoin de héros pour s'écrire. Parmi les vaillants équipiers, qui sera l'élu ?
            
            🎲 Oracle, sois notre guide.
            """
    }

    return page_dict

def data_URL():
    '''
    Set the URLs to the data sources.
    '''

    env_variables = load_configurations()

    data_dict = {
        'summarized_data_url': f'{env_variables["AWS_S3_URL"]}/geo_dvf_summarized_full.csv.gz',
        'datagouv_source_URL': env_variables["DATA_GOUV_URL"],
        'available_years_datagouv': list(np.arange(2018,2023+1)),
        'scrapped_year_current': f'{env_variables["AWS_S3_URL"]}/2024_merged/departements',
    }

    return data_dict

def firebase_credentials():
    '''
    Load configuration from .env file or from OS environment variables
    '''
    
    # List of required keys in lowercase
    keys_list = [
        'type', 'project_id', 'private_key_id', 'private_key', 'client_email',
        'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
        'client_x509_cert_url', 'universe_domain'
    ]
    
    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f'Missing or empty value for key: {key}')
            cred_dict[key] = value

        # Add prefix and suffix for the private_key
        cred_dict['private_key'] = cred_dict["private_key"].replace("/breakline/", "\n")
    except ValueError as e:
        print(f'Configuration error: {e}')
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict

def bigquery_credentials():
    env_variables = load_configurations()

    # Configuration de l'authentification avec variables d'environnement
    credentials_dict = {
        "type": env_variables.get('BIGQUERY_TYPE'),
        "project_id": env_variables.get('BIGQUERY_PROJECT_ID'),
        "private_key_id": env_variables.get('BIGQUERY_PRIVATE_KEY_ID'),
        "private_key": env_variables.get('BIGQUERY_PRIVATE_KEY').replace("/breakline/", "\n"),
        "client_email": env_variables.get('BIGQUERY_CLIENT_EMAIL'),
        "client_id": env_variables.get('BIGQUERY_CLIENT_ID'),
        "auth_uri": env_variables.get('BIGQUERY_AUTH_URI'),
        "token_uri": env_variables.get('BIGQUERY_TOKEN_URI'),
        "auth_provider_x509_cert_url": env_variables.get('ABIGQUERY_UTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": env_variables.get('BIGQUERY_CLIENT_X509_CERT_URL')
    }

    return credentials_dict

def azure_credentials():

    keys_list = [
        'AZURE_SERVER', 'AZURE_DATABASE', 'AZURE_UID', 'AZURE_PWD', 'AZURE_TABLE'
    ]

    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f'Missing or empty value for key: {key}')
            cred_dict[key] = value
    except ValueError as e:
        print(f'Configuration error: {e}')
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict

def AWS_credentials():
    keys_list = [
        'AWS_S3_URL'
    ]

    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f'Missing or empty value for key: {key}')
            cred_dict[key] = value
    except ValueError as e:
        print(f'Configuration error: {e}')
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict