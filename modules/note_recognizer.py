# note_recognizer.py
import wave
import numpy as np
import math

# Liste mit Notennamen
noten = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def lese_wav(pfad):
    """Liest WAV-Datei und gibt sample_rate und Daten zurück"""
    with wave.open(pfad, "rb") as w:
        sr = w.getframerate()
        frames = w.getnframes()
        daten = np.frombuffer(w.readframes(frames), dtype=np.int16)
        return sr, daten.astype(float)

def finde_freq(daten, sr):
    """Sucht die lauteste Frequenz im Signal"""
    fenster = np.hanning(len(daten))
    fft = np.fft.rfft(daten * fenster)
    freqs = np.fft.rfftfreq(len(daten), 1 / sr)
    idx = np.argmax(np.abs(fft))
    return freqs[idx]

def freq_zu_note(freq):
    """Rechnet Frequenz in Note um"""
    a4 = 440
    if freq <= 0:
        return "?"
    halbtöne = 12 * math.log2(freq / a4)
    halb_rund = int(round(halbtöne))
    midi = 69 + halb_rund
    name = noten[midi % 12]
    oktave = midi // 12 - 1
    return f"{name}{oktave}"

def erkenne_note(pfad):
    """Gesamter Ablauf"""
    try:
        sr, daten = lese_wav(pfad)
        freq = finde_freq(daten, sr)
        note = freq_zu_note(freq)
        return note, round(freq, 2)
    except Exception as e:
        print("Fehler:", e)
        return None, 0
