from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.text import LabelBase # Schriftarten verwenden
from modules import play_sounds, note_recognizer, sound_recorder # Eigene Skripte


#globale variable
darkmode = False

# Schriftart einbetten
LabelBase.register(
    name="Roboto", 
    fn_regular="assets/fonts/Roboto-Regular.ttf",
    fn_bold="assets/fonts/Roboto-Bold.ttf"
)

# Screens definieren
class PlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = AnchorLayout(
            anchor_x='center',  # horizontal zentrieren
            anchor_y='center'      # oben ausrichten
        )
        # Button erstellen
        play_button = Button(
            background_normal="assets/images/play-button.png",
            size_hint=(0.4, 0.15),  
            on_press=lambda x: print()
        )
        layout.add_widget(play_button)
        # Layout dem Screen hinzufügen
        self.add_widget(layout)

class RecognizeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Hier kannst du Noten erkennen"))


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(
            text="Einstellungen\n",
            size_hint=(0.8, 0.10)
        ))# Überschrift
        layout.add_widget(Button(
            text="About",
            on_press=self.show_about,
            size_hint=(0.8, 0.10),
            background_normal='',
            background_color=(0,0,1,1)
        ))# About btn
        layout.add_widget(Button(
        text="toggle\nDark-Mode",
            on_press=self.toggle_dark_mode,
            size_hint=(0.8, 0.10),
            background_normal='',
            background_color=(0,0,1,1)
        ))# Darkmode btn
        
        self.add_widget(layout) #Layout zum Screen hinzufügen

    def show_about(self, *args):
        popup = Popup(
            title="About",
            content=Label(text="Diese App wurde von\n Nils erstellt.\nVersion 1.0"),
            size_hint=(0.7, 0.4)  
            )
        popup.open()
    
    def toggle_dark_mode(self, *args):
        global darkmode
        darkmode = not darkmode
        #print(f"darkmode: {darkmode}")


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical')

        # ScreenManager erstellen
        self.sm = ScreenManager()
        self.sm.add_widget(PlayScreen(name="play"))
        self.sm.add_widget(RecognizeScreen(name="recognize"))
        self.sm.add_widget(SettingsScreen(name="settings"))

        # Startscreen
        self.sm.current = "play"

        main_layout.add_widget(self.sm)

        # Bottom Bar
        bottom_bar = BoxLayout(size_hint_y=0.15)

        btn_play = Button(background_normal="assets/images/play-button.png")
        btn_recognize = Button(background_normal="assets/images/home.png")
        btn_settings = Button(background_normal="assets/images/setting.png")

        buttons: dict = {
            btn_play: "play",
            btn_recognize: "recognize",
            btn_settings: "settings"
        }
        # Button Funktionen und an bottom_bar übergeben
        for btn, screen_name in buttons.items():
            bottom_bar.add_widget(btn)
            btn.bind(on_press=lambda x, name=screen_name: self.switch_screen(name))


        main_layout.add_widget(bottom_bar)
        return main_layout

    def switch_screen(self, screen_name):
        self.sm.current = screen_name

if __name__ == "__main__":
    MyApp().run()
