import os
from plyer import audio
from time import sleep

def record_audio(label, filename="recording.wav", duration=3): #duration in s
    # Android/Windows Ordner erstellen
    base_dir = os.path.join(os.getcwd(), "assets", "audio")
    os.makedirs(base_dir, exist_ok=True)

    filepath = os.path.join(base_dir, filename)

    audio.recorder.start(filepath)
    sleep(duration)
    audio.recorder.stop()
    return filepath
