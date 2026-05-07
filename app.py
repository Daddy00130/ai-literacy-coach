import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import io
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Learner Coach", page_icon="🇰🇪", layout="wide")

# Custom CSS for high-end look
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .heard-text {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        background: #E0E7FF;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- WORD BANK ---
word_bank = [
    {"word": "Elephant", "syllable": "EL-e-phant", "sentence": "The elephant is the largest animal in the Savannah.", "pattern": "ph"},
    {"word": "Alphabet", "syllable": "AL-pha-bet", "sentence": "There are 26 letters in the alphabet.", "pattern": "ph"},
    {"word": "Dolphin", "syllable": "DOL-phin", "sentence": "A dolphin is a very smart sea animal.", "pattern": "ph"},
    {"word": "Phone", "syllable": "PHONE", "sentence": "I use a phone to call my family.", "pattern": "ph"},
    {"word": "Photo", "syllable": "PHO-to", "sentence": "I took a photo of the beautiful sunset.", "pattern": "ph"},
    {"word": "Graph", "syllable": "GRAPH", "sentence": "We drew a graph in our math class today.", "pattern": "ph"},
    {"word": "Shoes", "syllable": "SHOES", "sentence": "I need to tie my shoes before I run.", "pattern": "sh"},
    {"word": "Three", "syllable": "THREE", "sentence": "Two plus one equals three.", "pattern": "th"},
    {"word": "Knife", "syllable": "KNIFE", "sentence": "Be careful when using a sharp knife.", "pattern": "kn"}
]

# --- SESSION STATE ---
if 'target_word' not in st.session_state:
    st.session_state.current_data = random.choice(word_bank)
    st.session_state.target_word = st.session_state.current_data["word"]
    if 'score' not in st.session_state: st.session_state.score = 0

data = st.session_state.current_data
target = st.session_state.target_word

# --- UI LAYOUT ---
with st.sidebar:
    st.title("📊 Progress Tracker")
    st.metric(label="Words Mastered", value=st.session_state.score)
    st.progress(st.session_state.score / 10 if st.session_state.score < 10 else 1.0)
    if st.button("Reset Session"):
        st.session_state.score = 0
        del st.session_state['target_word']
        st.rerun()

st.title("🇰🇪 AI Literacy Coach")

col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        st.subheader("Step 1: Listen")
        if st.button(f"🔊 Tap to hear AI sound"):
            tts = gTTS(text=target, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp)

        st.divider()
        
        st.subheader("Step 2: Speak")
        st.write("Click and say the word loudly:")
        # THE AI SPEECH ENGINE
        heard_text = speech_to_text(language='en', start_prompt="🎤 Start AI Recording", key='voice_input')

with col2:
    with st.container(border=True):
        st.subheader("AI Recognition Result")
        if heard_text:
            # THIS IS THE PART YOU WANTED: Clearly writing down what was spoken
            st.markdown(f'<div class="heard-text">AI Heard: "{heard_text}"</div>', unsafe_allow_html=True)
            
            if heard_text.lower() == target.lower():
                st.success("✅ MATCH! Perfect Pronunciation.")
            else:
                st.error("❌ NOT A MATCH. Try again!")
                st.warning(f"💡 Suggestion: Stress it like **{data['syllable']}**")
        else:
            st.info("Waiting for you to speak...")

st.divider()

# --- SPELLING SECTION ---
st.subheader("Step 3: Spelling & Pattern Check")
user_spell = st.text_input("How do you spell the word you just said?", placeholder="Type here...").strip()

if user_spell:
    if user_spell.lower() == target.lower():
        st.balloons()
        st.success(f"🎊 Excellent! You spelled **{target}** correctly!")
        if st.button("Move to Next Word ➡️"):
            st.session_state.score += 1
            del st.session_state['target_word']
            st.rerun()
    elif "f" in user_spell.lower() and data['pattern'] == "ph":
        st.error(f"⚠️ Pattern Alert: Remember, in '{target}', the 'f' sound is made by 'PH'.")
    else:
        st.error("Keep trying! You are getting closer.")

# --- CONTEXT ---
with st.expander("Show Sentence Context & Meaning"):
    st.write(f"📝 **Usage:** {data['sentence']}")