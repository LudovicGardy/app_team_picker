import streamlit as st
from modules.database import Database
from typing import Any, Callable

def init_page_config(page_config): ### Must be called before any other st. function
    st.set_page_config(page_title=page_config().get('page_title'), 
                page_icon = page_config().get('page_icon'),  
                layout = page_config().get('layout'),
                initial_sidebar_state = page_config().get('initial_sidebar_state'))

def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 

def init_session_state():
    st.session_state['database'] = Database()

def display_sidebar(page_config:Callable):
    try:
        logo_path = page_config().get('page_logo')
    except FileNotFoundError:
        raise FileNotFoundError("page_logo path not found")

    desired_width = 60

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image(logo_path, width=desired_width)
    with col2:
        st.write(page_config().get('sidebar_title'))

    st.caption(page_config().get('page_description'))
    st.divider()