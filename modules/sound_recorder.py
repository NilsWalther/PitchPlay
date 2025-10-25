import os
import threading

try:
    import sounddevice as sd
    import soundfile as sf
    desktop = True
except:
    desktop = False

try:
    from plyer import audio
    android = True
except:
    android = False

audio_ordner = "assets/audio"
os.makedirs(audio_ordner, exist_ok=True)
datei = os.path.join(audio_ordner, "recording.wav")

aufnehmen = False

def start_record():
    global aufnehmen
    if android:
        audio.start()
        aufnehmen = True
    elif desktop:
        threading.Thread(target=record_pc).start()
        aufnehmen = True
    else:
        print("Kein Audio-Modul gefunden.")
    return aufnehmen

def stop_record():
    global aufnehmen
    if android:
        audio.stop()
    elif desktop:
        aufnehmen = False
    return aufnehmen

def record_pc():
    global aufnehmen
    aufnehmen = True
    sr = 44100
    with sf.SoundFile(datei, mode='w', samplerate=sr, channels=1) as f:
        with sd.InputStream(samplerate=sr, channels=1) as s:
            while aufnehmen:
                data, _ = s.read(1024)
                f.write(data)
