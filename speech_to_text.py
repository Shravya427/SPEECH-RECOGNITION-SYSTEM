import speech_recognition as sr
import os
from datetime import datetime

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

def record_audio(recognizer, source):
    """Listen until silence is detected after speech begins."""
    print("🎙️ Calibrating microphone... Please stay silent.")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("🎙️ Speak now...")
    audio = recognizer.listen(source)
    print("🔊 Audio captured, transcribing...")
    return audio

def save_audio(audio_data, directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(directory, f"audio_{timestamp}.wav")
    with open(path, "wb") as f:
        f.write(audio_data.get_wav_data())
    print(f"✅ Audio saved as '{path}'")
    return path

def save_transcription(text, directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(directory, f"transcription_{timestamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"📝 Transcription saved as '{path}'")
    return path

def transcribe_audio(audio, recognizer):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ Google Speech Recognition error: {e}")
    return None

def main():
    recognizer = sr.Recognizer()
    script_dir = get_script_directory()

    try:
        with sr.Microphone() as source:
            audio = record_audio(recognizer, source)
            save_audio(audio, script_dir)

            text = transcribe_audio(audio, recognizer)
            if text:
                print("🗣️ You said:", text)
                save_transcription(text, script_dir)

    except sr.WaitTimeoutError:
        print("⏳ No speech detected.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()

