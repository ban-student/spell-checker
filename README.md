# spell-checker
import streamlit as st
import openai
import pyttsx3
import speech_recognition as sr
from spellchecker import SpellChecker
import language_tool_python
from symspellpy import SymSpell
import os

# ✅ Streamlit Page Configuration
st.set_page_config(page_title="AI Spell & Grammar Checker", page_icon="📝", layout="centered")

# ✅ Load Spellchecker & Grammar Tools Efficiently
@st.cache_resource
def initialize_tools():
    spell_checker = SpellChecker()
    grammar_tool = language_tool_python.LanguageTool('en-US')
    hindi_spell_checker = SymSpell()
    dict_path = "hindi_words.txt"
    if os.path.exists(dict_path):
        hindi_spell_checker.load_dictionary(dict_path, term_index=0, count_index=1, separator="\t")
    return spell_checker, grammar_tool, hindi_spell_checker

spell_checker, grammar_tool, hindi_spell_checker = initialize_tools()

# ✅ Function to Speak Text
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ✅ Function to Capture Microphone Input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='hi')
            return text
        except sr.UnknownValueError:
            return "❌ Could not understand the audio."
        except sr.RequestError:
            return "❌ Speech recognition service is unavailable."

# ✅ OpenAI API Key (Replace with a secure method in production)
OPENAI_API_KEY = "your-api-key-here"
openai.api_key = OPENAI_API_KEY

# ✅ Title
st.markdown("<h1 style='text-align: center; color: #FF9800;'>📝 AI Spell & Grammar Checker</h1>", unsafe_allow_html=True)

# ✅ Session State for Text Persistence
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "speak_corrected" not in st.session_state:
    st.session_state.speak_corrected = False
if "speak_ai" not in st.session_state:
    st.session_state.speak_ai = False

# ✅ Microphone Input Button
if st.button("🎤 Speak Input"):
    spoken_text = recognize_speech()
    if "❌" not in spoken_text:
        st.session_state.user_text = spoken_text
    else:
        st.warning(spoken_text)

# ✅ User Input (Text Area)
st.session_state.user_text = st.text_area("Enter text below:", st.session_state.user_text, height=200)

# ✅ Function for Real-Time Corrections
def correct_text(text):
    if not text.strip():
        return "", [], []
    
    words = text.split()
    misspelled_words = spell_checker.unknown(words)
    
    corrected_text = text
    spelling_fixes = []
    for word in misspelled_words:
        best_suggestion = spell_checker.correction(word) or word
        corrected_text = corrected_text.replace(word, best_suggestion)
        spelling_fixes.append(f"❌ {word} ➝ ✅ {best_suggestion}")
    
    grammar_issues = grammar_tool.check(corrected_text)
    if grammar_issues:
        corrected_text = language_tool_python.utils.correct(corrected_text, grammar_issues)
    
    return corrected_text, spelling_fixes, grammar_issues

# ✅ Function for Hindi Autocorrection
def correct_hindi_text(text):
    if not text.strip():
        return ""
    corrected_text = ""
    words = text.split()
    for word in words:
        suggestions = hindi_spell_checker.lookup(word, verbosity=0, max_edit_distance=2)
        if suggestions:
            corrected_text += suggestions[0].term + " "
        else:
            corrected_text += word + " "
    return corrected_text.strip()

# ✅ Function for AI-Based Enhancement
def enhance_text_with_ai(text):
    if not text.strip():
        return "⚠ Please enter some text."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Improve the following text while keeping its meaning:\n{text}"}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Real-Time Processing
corrected_text, spelling_fixes, grammar_issues = correct_text(st.session_state.user_text)
hindi_corrected_text = correct_hindi_text(st.session_state.user_text)

st.subheader("✅ Auto-Corrected Text:")
st.text_area("Corrected Output:", corrected_text, height=200)

st.subheader("✅ Hindi Auto-Corrected Text:")
st.text_area("Hindi Corrected Output:", hindi_corrected_text, height=200)

if st.button("🔊 Listen to Corrected Text"):
    st.session_state.speak_corrected = True
    st.rerun()

if st.session_state.speak_corrected:
    speak_text(corrected_text)
    st.session_state.speak_corrected = False
    st.rerun()

if spelling_fixes:
    st.subheader("🔴 Spelling Corrections:")
    for fix in spelling_fixes:
        st.markdown(fix, unsafe_allow_html=True)

if grammar_issues:
    st.subheader("🟡 Grammar Corrections:")
    for issue in grammar_issues:
        st.markdown(f"🔴 Error: {issue.context}", unsafe_allow_html=True)
        st.markdown(f"💡 Suggestion: <span style='color:green'>{', '.join(issue.replacements)}</span>", unsafe_allow_html=True)

# ✅ AI Text Enhancement
if st.session_state.user_text.strip():
    improved_text = enhance_text_with_ai(st.session_state.user_text)
    st.subheader("✨ AI-Enhanced Version:")
    st.text_area("AI-Suggested Output:", improved_text, height=200)

    if st.button("🔊 Listen to AI-Enhanced Text"):
        st.session_state.speak_ai = True
        st.rerun()

    if st.session_state.speak_ai:
        speak_text(improved_text)
        st.session_state.speak_ai = False
        st.rerun()
