"""
Grammar checking and correction using LanguageTool.
"""
import language_tool_python


def get_grammar_tool(lang_code: str = "en-US"):
    """Loads LanguageTool. Needs Java installed, downloads model on first run."""
    return language_tool_python.LanguageTool(lang_code)


def check_grammar(text: str, tool) -> tuple[str, list[dict]]:
    """
    Return (corrected text, list of issue details) for the given text.
    """
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)

    details = [
        {
            "message": m.message,
            "context": m.context,
            "replacements": m.replacements[:5],
        }
        for m in matches
    ]
    return corrected_text, details
