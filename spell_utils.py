"""
English spell checking (PySpellChecker) and Hindi spell checking (SymSpell).
"""
import os
from spellchecker import SpellChecker
from symspellpy import SymSpell, Verbosity

_HINDI_DICT_PATH = os.path.join(os.path.dirname(__file__), "data", "hindi_dictionary.txt")
_ENGLISH_EXTRA_WORDS_PATH = os.path.join(os.path.dirname(__file__), "data", "english_extra_words.txt")


def get_english_spellchecker() -> SpellChecker:
    """PySpellChecker + extra words from data/english_extra_words.txt"""

    spell = SpellChecker()
    if os.path.exists(_ENGLISH_EXTRA_WORDS_PATH):
        spell.word_frequency.load_text_file(_ENGLISH_EXTRA_WORDS_PATH)
    return spell


def check_english_spelling(text: str, spell: SpellChecker) -> dict:
    """
    Return a dict of {misspelled word: suggested correction} for the given text.
    """
    words = [w.strip(".,!?;:\"'()") for w in text.split()]
    words = [w for w in words if w]

    misspelled = spell.unknown(words)
    corrections = {}
    for word in misspelled:
        suggestion = spell.correction(word)
        if suggestion and suggestion != word:
            corrections[word] = suggestion
    return corrections


def get_hindi_spellchecker(max_edit_distance: int = 3) -> SymSpell:
    """Loads the Hindi dictionary into SymSpell. Distance 3 works better
    than the default 2 for Hindi since conjunct letters need more edits."""

    sym_spell = SymSpell(max_dictionary_edit_distance=max_edit_distance, prefix_length=7)
    if os.path.exists(_HINDI_DICT_PATH):
        sym_spell.load_dictionary(_HINDI_DICT_PATH, term_index=0, count_index=1, encoding="utf-8")
    return sym_spell


def check_hindi_spelling(text: str, sym_spell: SymSpell) -> dict:
    """
    Return a dict of {misspelled word: suggested correction} for Hindi text.
    """
    corrections = {}
    for word in text.split():
        clean_word = word.strip("।,.!?;:\"'()")
        if not clean_word:
            continue
        suggestions = sym_spell.lookup(clean_word, Verbosity.CLOSEST, max_edit_distance=3)
        if suggestions and suggestions[0].term != clean_word:
            corrections[clean_word] = suggestions[0].term
    return corrections
