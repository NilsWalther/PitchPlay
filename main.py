# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.clock import Clock
import threading
import os
from modules import sound_recorder, note_recognizer

# Pfad für gespeicherte Aufnahmen
audio_pfad = os.path.join("assets", "audio", "recording.wav")

# Font initialisieren
LabelBase.register(
    name="MeineSchrift",
    fn_regular="assets/fonts/Roboto-Regular.ttf",
    fn_bold="assets/fonts/Roboto-Bold.ttf"
)

# --- Seiten der App ---

class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=15, padding=15)
        layout.add_widget(Label(text="Wiedergabe (noch leer)", font_size=22, font_name="MeineSchrift"))
        layout.add_widget(Label(text="Hier kann man Aufnahmen abspielen (gespeicherte).", font_size=16, font_name="MeineSchrift"))
        self.add_widget(layout)


class RecordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recording = False

        self.layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        self.info = Label(text="Drücke das Mikrofon, um aufzunehmen", font_size=18, font_name="MeineSchrift")
        self.layout.add_widget(self.info)

        self.btn = Button(
            text="Aufnahme starten",
            size_hint=(1, 0.3),
            background_color=(1, 0.4, 0.4, 1),
            font_name="MeineSchrift"
        )
        self.btn.bind(on_press=self.toggle_record)
        self.layout.add_widget(self.btn)

        self.result = Label(text="", font_size=20, font_name="MeineSchrift")
        self.layout.add_widget(self.result)
        self.add_widget(self.layout)

    def toggle_record(self, *args):
        # Aufnahme starten oder stoppen
        if not self.recording:
            self.info.text = "Aufnahme läuft..."
            self.btn.text = "Aufnahme stoppen"
            self.btn.background_color = (1, 0.2, 0.2, 1)
            sound_recorder.start_record()
            self.recording = True
        else:
            sound_recorder.stop_record()
            self.info.text = "Verarbeite Aufnahme..."
            self.btn.text = "Aufnahme starten"
            self.btn.background_color = (0.3, 0.8, 0.3, 1)
            self.recording = False
            threading.Thread(target=self.analyse_note).start()

    def analyse_note(self):
        import time
        time.sleep(0.5)
        note, freq = note_recognizer.erkenne_note(audio_pfad)
        if note == "?" or note is None:
            text = "Keine Note erkannt"
        else:
            text = f"Erkannte Note: [b]{note}[/b]\nFrequenz: {freq} Hz"
        # Text im Haupt-Thread aktualisieren
        Clock.schedule_once(lambda dt: self.update_result(text))

    def update_result(self, text):
        self.info.text = "Fertig!"
        self.result.markup = True
        self.result.text = text


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation='vertical', spacing=15, padding=15)
        box.add_widget(Label(text="Einstellungen", font_size=22, font_name="MeineSchrift"))

        btn_about = Button(text="Über die App", size_hint=(1, 0.2), font_name="MeineSchrift")
        btn_about.bind(on_press=self.show_about)
        box.add_widget(btn_about)

        btn_exit = Button(text="Beenden", size_hint=(1, 0.2), font_name="MeineSchrift")
        btn_exit.bind(on_press=lambda x: App.get_running_app().stop())
        box.add_widget(btn_exit)

        self.add_widget(box)

    def show_about(self, *args):
        pop = Popup(
            title="Über die App",
            content=Label(text="Noten-Erkenner v1.0\nErstellt mit Kivy\nvon Nils", font_name="MeineSchrift"),
            size_hint=(0.8, 0.4)
        )
        pop.open()


# --- HauptApp ---
class NoteApp(App):
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(PlayScreen(name="play"))
        self.sm.add_widget(RecordScreen(name="record"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        # Hauptlayout 
        root = BoxLayout(orientation='vertical')

        # oben
        root.add_widget(self.sm)

        # untere Leiste
        nav = BoxLayout(size_hint_y=0.12, spacing=10, padding=10)

        btn_play = Button(text="", background_normal="assets/images/play-button.png" ,on_press=lambda x: self.switch_to("play"), font_name="MeineSchrift")
        btn_rec = Button(text="", background_normal="",on_press=lambda x: self.switch_to("record"), font_name="MeineSchrift")
        btn_set = Button(text="", background_normal="assets/images/setting.png",on_press=lambda x: self.switch_to("settings"), font_name="MeineSchrift")

        for b in [btn_play, btn_rec, btn_set]:
            b.font_size = 28
            b.background_color = (1,1,1,1)
            nav.add_widget(b)

        root.add_widget(nav)

        self.sm.current = "record"
        return root

    def switch_to(self, name):
        self.sm.current = name


if __name__ == "__main__":
    NoteApp().run()
