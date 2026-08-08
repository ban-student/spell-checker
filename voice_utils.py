"""
Speech-to-text (SpeechRecognition) and text-to-speech (pyttsx3) helpers.
"""
import speech_recognition as sr
import pyttsx3


def transcribe_from_microphone(language: str = "en-IN", timeout: int = 5) -> str:
    """
    Record from the default microphone and return the transcribed text.
    language examples: "en-IN", "en-US", "hi-IN"
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as exc:
        raise RuntimeError(f"Speech recognition service error: {exc}") from exc


def speak_text(text: str, rate: int = 170) -> None:
    """Speak the given text aloud using the offline pyttsx3 engine."""
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
