# AI Spell & Grammar Checker

A voice-enabled spell and grammar checker for English and Hindi, built with Streamlit.

Made for *Ideathon 2.0: Lingua Hack*, Mayukh Fest, Banasthali Vidyapith —  3rd place.

## Problem Statement

- Multilingual writing (especially English + Hindi) is hard to get right, especially for students and non-native speakers
- Most free spell checkers only support English well
- Few tools combine spelling, grammar, and voice input in one place
- Basic dictionary-based checkers can't fix context-dependent errors (like a typo that happens to form a different real word)

## Solution

- Built a Streamlit web app combining spelling, grammar, and AI-based correction in one interface
- English: PySpellChecker for spelling, LanguageTool for grammar
- Hindi: SymSpell with a custom dictionary (built from Bhashini/Vatika text corpora, since off-the-shelf Hindi grammar tools are limited)
- Added Gemini AI to catch context-based errors neither rule-based tool can — and to handle Hindi grammar checking, since LanguageTool has no Hindi rules at all
- Added voice input/output using SpeechRecognition and pyttsx3 for accessibility

## What it does
- Checks English spelling and grammar
- Checks Hindi spelling, with grammar correction via Gemini (LanguageTool doesn't support Hindi grammar rules)
- Voice input (speak instead of typing) and text-to-speech for corrected output
- AI-powered rewrite for clarity and fluency

## Tech stack
- Python + Streamlit
- PySpellChecker (English spelling)
- SymSpell (Hindi spelling, custom dictionary built from Bhashini/Vatika datasets)
- LanguageTool (English grammar)
- Google Gemini API (AI text enhancement + Hindi grammar)
- SpeechRecognition + pyttsx3 (voice input/output)

## Setup
Requires Python 3.9+ and Java (needed by LanguageTool).

```bash
git clone https://github.com/ban-student/spell-checker.git
cd spell-checker
python -m venv venv
venv\Scripts\activate      
pip install -r requirements.txt
streamlit run app.py
```
To use AI enhancement, get a free Gemini API key from [aistudio.google.com](https://aistudio.google.com) and paste it into the sidebar when running the app.

## Known issues
- Voice input only works when running locally (needs a real microphone)
- Hindi spelling suggestions aren't always perfect since the dictionary is dataset-derived, not exhaustive
- LanguageTool's public grammar API has a rate limit — running it locally avoids this