import speech_recognition as sr
import tempfile


def tamil_voice_input(audio_bytes):

    recognizer = sr.Recognizer()


    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )


    file.write(audio_bytes)

    file.close()


    with sr.AudioFile(file.name) as source:

        audio = recognizer.record(source)


    text = recognizer.recognize_google(
        audio,
        language="ta-IN"
    )


    return text