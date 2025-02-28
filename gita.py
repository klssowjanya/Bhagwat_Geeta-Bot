#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import google.generativeai as genai
import pandas as pd
import random

# Configure Gemini
genai.configure(api_key="AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c")
model = genai.GenerativeModel('gemini-pro')

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('bhagwatgeeta.csv')  # Update with your filename

df = load_data()

# Session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: Example questions
with st.sidebar:
    st.markdown("## 🕉️ Dharma Compass")
    example_questions = [
        "How to deal with anxiety according to Chapter 2?",
        "What is the nature of the eternal soul?",
        "Explain the concept of karma yoga",
        "Teachings about mind control",
        "Verses about overcoming fear"
    ]
    
    selected_question = st.radio("Select a sample inquiry:", example_questions, index=None)

# Get user query from chat input
user_query = selected_question if selected_question else st.chat_input("Ask your spiritual question...")

def generate_gita_response(user_query):
    """Generate response based on Bhagavad Gita wisdom."""
    if not user_query:
        return None

    try:
        response = model.generate_content(user_query)
        return response.text
    except Exception as e:
        return "I'm unable to process your request now. Please try again later."

if user_query:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Generate bot response
    with st.spinner('Meditating on the Gita...'):
        bot_response = generate_gita_response(user_query)

    # Add bot response to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
