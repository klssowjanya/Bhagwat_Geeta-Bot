#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1589994965851-a8f479c573a9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    .header {
        color: #FFD700;
        text-align: center;
        padding: 2rem;
        background: rgba(0,0,0,0.7);
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .divider {
        border-top: 2px solid #4CAF50;
        margin: 1.5rem 0;
    }
    .chat-message {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def is_offensive_or_irrelevant(query):
    """Detect non-spiritual queries using contextual analysis"""
    spiritual_keywords = [
        'gita', 'krishna', 'dharma', 'yoga', 'karma', 'soul', 'meditation',
        'peace', 'wisdom', 'verse', 'chapter', 'arjuna', 'bhagavad', 'teaching',
        'life', 'purpose', 'mind', 'action', 'devotion', 'scripture'
    ]
    
    # Check for spiritual context
    if not any(keyword in query.lower() for keyword in spiritual_keywords):
        return True
    
    # Use Gemini's safety filters
    safety_settings = {
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_MEDIUM_AND_ABOVE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_MEDIUM_AND_ABOVE'
    }
    
    try:
        safety_check = model.generate_content(
            f"Does this query require spiritual guidance? Answer only YES/NO: {query}",
            safety_settings=safety_settings
        )
        return "yes" not in safety_check.text.lower()
    except:
        return True

def create_guidance_response():
    """Generate compassionate redirection using Gita verses"""
    guidance_options = [
        ("BG 2.50", "One who is equipoised in success and failure is wise. Let's discuss how to cultivate this equanimity."),
        ("BG 6.5", "Elevate yourself through your own mind. Would you like guidance on self-improvement?"),
        ("BG 12.13", "One who is free from ill-will is dear to the Lord. How can I help you cultivate positive thoughts?"),
        ("BG 2.14", "The wise are unmoved by heat and cold, pleasure and pain. Shall we explore this stability?"),
        ("BG 3.37", "It is desire that leads to anger. Would you like to discuss overcoming negative emotions?")
    ]
    verse_ref, advice = random.choice(guidance_options)
    return f"**{verse_ref} teaches**: {advice}"

def get_context(chapter=None, verse=None, keyword=None):
    """Retrieve relevant context from dataset"""
    try:
        if chapter and verse:
            result = df[(df['Chapter'] == chapter) & (df['Verse'] == verse)]
            return result.to_dict('records')
        elif keyword:
            return df[df['EngMeaning'].str.contains(keyword, case=False)].head(3).to_dict('records')
        return None
    except:
        return None

def generate_gita_response(user_query):
    if is_offensive_or_irrelevant(user_query):
        return create_guidance_response()
    
    # Extract chapter/verse numbers
    chapter, verse = None, None
    words = user_query.lower().replace(',', ' ').split()
    
    for i, word in enumerate(words):
        if word in ['chapter', 'ch'] and i+1 < len(words):
            try: chapter = int(words[i+1])
            except: pass
        if word in ['verse', 'vs'] and i+1 < len(words):
            try: verse = int(words[i+1])
            except: pass

    # Get context from dataset
    context_data = get_context(chapter, verse) or get_context(keyword=user_query)
    
    if not context_data:
        return "The divine wisdom is vast. Could you please rephrase or ask about a specific teaching?"
    
    # Create grounded prompt
    prompt = f"""You are a Bhagavad Gita scholar. Use ONLY this context:
    {context_data}

    Answer this query: {user_query}

    Format rules:
    - Start with relevant verse reference if available
    - Keep response under 100 words
    - Include practical application
    - Use simple, compassionate language
    - If unsure, suggest consulting a spiritual teacher
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "The divine wisdom flows in mysterious ways. Please ask again with a focused mind."

# App Header
st.markdown("""
<div class="header">
    <h1>🌿 Bhagavad Gita Wisdom Companion 🌼</h1>
    <h3>Discover Eternal Truths • Cultivate Inner Peace • Awaken Consciousness</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar with Spiritual Guidance
with st.sidebar:
    st.markdown("## 🕉️ Dharma Compass")
    st.markdown("""
    **Five Principles for Inquiry:**
    1. Seek truth with pure intention
    2. Respect all paths to wisdom
    3. Cultivate self-awareness
    4. Practice compassionate listening
    5. Embrace non-attachment
    """)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.markdown("**Sample Inquiries:**")
    example_questions = [
        "How to deal with anxiety according to Chapter 2?",
        "What is the nature of the eternal soul?",
        "Explain the concept of karma yoga",
        "Teachings about mind control",
        "Verses about overcoming fear"
    ]
    for q in example_questions:
        st.button(q, on_click=lambda q=q: st.session_state.update(question=q))

# Chat Interface
user_query = st.chat_input("Ask your spiritual question...", key="question")

if user_query:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    # Generate response
    with st.spinner('Meditating on the Gita...'):
        bot_response = generate_gita_response(user_query)
    
    # Add bot response to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(f"<div class='chat-message'>🙋 **Seeker:** {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message'>📜 **Wisdom:** {message['content']}</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
    .footer {
        text-align: center;
        padding: 1rem;
        background: rgba(0,0,0,0.7);
        color: white;
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
<div class="footer">
    <p>🕉️ "For one who has conquered the mind, the mind is the best of friends" - Bhagavad Gita 6.6 🕉️</p>
</div>
""", unsafe_allow_html=True)

