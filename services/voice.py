from gtts import gTTS
import tempfile


# Maps app language names to gTTS language codes
TTS_LANG_CODES = {
    "தமிழ்": "ta",
    "हिन्दी": "hi",
    "English": "en"
}


def speak_tamil(text):
    """
    Kept for backward compatibility — always speaks in Tamil.
    """
    return speak_text(text, "தமிழ்")


def speak_text(text, language):
    """
    Generic text-to-speech for any supported app language
    (English / தமிழ் / हिन्दी).
    """

    if not text:
        return None

    lang_code = TTS_LANG_CODES.get(language, "en")

    audio_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts = gTTS(
        text=text,
        lang=lang_code
    )

    tts.save(audio_file.name)

    return audio_file.name