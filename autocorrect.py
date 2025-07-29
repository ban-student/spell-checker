import streamlit as st
from spellchecker import SpellChecker
import language_tool_python  # For grammar and sentence correction

# Initialize the spell checker and grammar tool
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')  # English language model

# Set Streamlit page configuration
st.set_page_config(page_title="Spell & Grammar Checker", page_icon="📝", layout="centered")

# Title
st.title("📝 Spell & Grammar Checker")

# Session State for Text Persistence
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Input Text Area
st.session_state.input_text = st.text_area("Enter Text:", st.session_state.input_text, height=200)

# Buttons Layout
col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Check Spelling & Grammar", use_container_width=True):
        if st.session_state.input_text.strip():
            words = st.session_state.input_text.split()
            misspelled = spell.unknown(words)

            # Spelling Corrections
            if not misspelled:
                st.success("✅ No spelling errors found!")
            else:
                corrections = {word: spell.correction(word) or word for word in misspelled}
                st.subheader("Spelling Corrections:")
                for word, correction in corrections.items():
                    st.markdown(f"*❌ {word} ➝ ✅ {correction}*")

            # Grammar Corrections
            matches = tool.check(st.session_state.input_text)
            if matches:
                st.subheader("Grammar Corrections:")
                corrected_text = language_tool_python.utils.correct(st.session_state.input_text, matches)
                st.markdown(f"🔹 *Suggested Correction:*\n\n{corrected_text}")

                # Display detailed grammar suggestions
                for match in matches:
                    st.markdown(f"🔴 *Error:* {match.context}")
                    st.markdown(f"💡 *Suggestion:* {match.replacements}")
                    st.markdown("---")

        else:
            st.warning("⚠️ Please enter some text.")

with col2:
    if st.button("❌ Clear", use_container_width=True):
        st.session_state.input_text = ""  # Reset the input field
        st.experimental_rerun()  # Refresh page
