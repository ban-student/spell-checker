import streamlit as st

from spell_utils import (
    get_english_spellchecker,
    check_english_spelling,
    get_hindi_spellchecker,
    check_hindi_spelling,
)
from grammar_utils import get_grammar_tool, check_grammar
from voice_utils import transcribe_from_microphone, speak_text
from ai_utils import enhance_text

st.set_page_config(page_title="AI Spell & Grammar Checker", page_icon="📝", layout="centered")


# Cached resources (loaded once per server process, not once per rerun)
@st.cache_resource
def load_english_spellchecker():
    return get_english_spellchecker()


@st.cache_resource
def load_hindi_spellchecker():
    return get_hindi_spellchecker()


@st.cache_resource
def load_grammar_tool():
    return get_grammar_tool("en-US")


# Session state
for key, default in {
    "input_text": "",
    "corrected_text": "",
    "enhanced_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar
st.sidebar.title(" Settings")
language = st.sidebar.radio("Language", ["English", "Hindi"], index=0)
gemini_key = st.sidebar.text_input("Gemini API key (for AI enhancement)", type="password")
st.sidebar.caption(
    "Your key is kept only in this browser session and is never stored."
)

st.title(" AI Spell & Grammar Checker")
st.caption("Voice enabled, multilingual spell & grammar checking — English & Hindi.")

# Input area
st.session_state.input_text = st.text_area("Enter text:", st.session_state.input_text, height=200)

col_mic, col_check, col_clear = st.columns(3)

with col_mic:
    if st.button(" Speak", use_container_width=True):
        lang_code = "hi-IN" if language == "Hindi" else "en-IN"
        with st.spinner("Listening..."):
            try:
                transcript = transcribe_from_microphone(language=lang_code)
                if transcript:
                    st.session_state.input_text = (
                        st.session_state.input_text + " " + transcript
                    ).strip()
                    st.rerun()
                else:
                    st.warning(" Couldn't understand the audio. Please try again.")
            except Exception as exc:
                st.error(f"🔊 Microphone error: {exc}")

with col_check:
    run_check = st.button(" Check Spelling & Grammar", use_container_width=True)

with col_clear:
    if st.button(" Clear", use_container_width=True):
        st.session_state.input_text = ""
        st.session_state.corrected_text = ""
        st.session_state.enhanced_text = ""
        st.rerun()

# Spelling & grammar checking
if run_check:
    text = st.session_state.input_text.strip()
    if not text:
        st.warning(" Please enter some text.")
    elif language == "English":
        spell = load_english_spellchecker()
        spelling_corrections = check_english_spelling(text, spell)

        st.subheader("Spelling")
        if not spelling_corrections:
            st.success(" No spelling errors found!")
        else:
            for word, correction in spelling_corrections.items():
                st.markdown(f" **{word}** ➝  **{correction}**")

        tool = load_grammar_tool()
        corrected_text, grammar_details = check_grammar(text, tool)
        st.session_state.corrected_text = corrected_text

        st.subheader("Grammar")
        if not grammar_details:
            st.success(" No grammar issues found!")
        else:
            st.markdown(f"🔹 **Suggested correction:**\n\n{corrected_text}")
            for detail in grammar_details:
                st.markdown(f"-> *Error context:* {detail['context']}")
                st.markdown(f"-> *Suggestions:* {', '.join(detail['replacements']) or '—'}")
                st.markdown("---")

    else:  # Hindi
        sym_spell = load_hindi_spellchecker()
        hindi_corrections = check_hindi_spelling(text, sym_spell)
        corrected = text

        st.subheader("हिन्दी वर्तनी सुधार (Hindi Spelling)")
        if not hindi_corrections:
            st.success(" कोई वर्तनी त्रुटि नहीं मिली! (No spelling errors found!)")
        else:
            for word, correction in hindi_corrections.items():
                st.markdown(f" **{word}** ➝  **{correction}**")
                corrected = corrected.replace(word, correction)
            st.markdown(f"🔹 **Suggested correction:**\n\n{corrected}")

        st.session_state.corrected_text = corrected

        st.subheader("व्याकरण (Grammar)")
        st.caption(
            " Hindi grammar checking runs through the AI enhancement model (Gemini)."
        )
        if not gemini_key:
            st.warning(
                " Add your Gemini API key in the sidebar to get Hindi grammar correction."
            )
        else:
            with st.spinner("Checking Hindi grammar with AI..."):
                try:
                    # use raw text here, not the symspell output — symspell
                    # sometimes picks the wrong word so let gemini see the original
                    st.session_state.enhanced_text = enhance_text(text, api_key=gemini_key)
                except Exception as exc:
                    st.error(f"AI grammar check failed: {exc}")
            if st.session_state.enhanced_text:
                st.markdown(f" **AI-corrected version:**\n\n{st.session_state.enhanced_text}")

# AI-based text enhancement
st.divider()
st.subheader(" AI Text Enhancement")
enhance_source = st.session_state.corrected_text or st.session_state.input_text

if st.button("Improve clarity & fluency with AI", use_container_width=True):
    if not enhance_source.strip():
        st.warning(" Please enter and check some text first.")
    elif not gemini_key:
        st.warning(" Add your Gemini API key in the sidebar to use this feature.")
    else:
        with st.spinner("Enhancing text..."):
            try:
                st.session_state.enhanced_text = enhance_text(enhance_source, api_key=gemini_key)
            except Exception as exc:
                st.error(f"AI enhancement failed: {exc}")

if st.session_state.enhanced_text:
    st.markdown("**Enhanced version:**")
    st.write(st.session_state.enhanced_text)
    if st.button("🔊 Read enhanced text aloud"):
        try:
            speak_text(st.session_state.enhanced_text)
        except Exception as exc:
            st.error(f"Text to speech error: {exc}")
            