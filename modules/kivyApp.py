# -- coding: utf-8

import asyncio
import sqlite3

from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.audio import Sound
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

from kivy.config import Config

from dotenv import load_dotenv
from os import getenv, path


class MySlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 50
        self.max = 100
        self.min = 0
        self.size_hint_x = 0.3


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = 1500 * 0.01
        self.size_hint_x = 0.3


class StopStartButton(MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "stop"



class NextMusicButton(MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "next"



class PreviousMusicButton(MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "previous"


class SoundPlay(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = 0.06
        self.now_play = None

        self.previous_button = PreviousMusicButton()
        self.stop_button = StopStartButton()
        self.next_button = NextMusicButton()
        self.slider = MySlider()
        self.nameMusic = Label(font_size=1500 * 0.01, shorten=True, shorten_from="right")
        self.sound = Sound()
        self.position = 0

        self.slider.bind(value=self.set_sound)
        self.stop_button.bind(on_press=self.pauseButton)
        self.next_button.bind(on_press=self.skipButton)
        self.previous_button.bind(on_press=self.skipButton)

        self.add_widget(self.previous_button)
        self.add_widget(self.stop_button)
        self.add_widget(self.next_button)
        self.add_widget(self.nameMusic)
        self.add_widget(self.slider)

    def pauseButton(self, instance):
        if self.sound.state == "play":
            self.position = self.sound.get_pos()
            self.sound.stop()
            self.stop_button.text = "play"
        else:
            self.sound.seek(self.position)
            self.sound.play()
            self.stop_button.text = "stop"

    def skipButton(self, instance):
        if self.sound.state == "play":
            self.sound.stop()
        count = 1 if instance.text == "next" else -1
        ind = self.now_play.parent.parent.children.index(self.now_play.parent)
        if ind == len(self.now_play.parent.parent.children) - 1 and instance.text == "previous":
            ind = 0
            count = 0
        elif ind == 0 and instance.text == "next":
            ind = len(self.now_play.parent.parent.children) - 1
            count = 0
        self.now_play = self.now_play.parent.parent.children[ind - count].children[1]
        path_to_music = path.join(getenv("PATH_TO_MUSIC"), self.now_play.parent.children[0].text + ".mp3")
        self.nameMusic.text = self.now_play.text
        self.load_sound(path_to_music)

    def load_sound(self, path_to_music: str):
        self.sound = SoundLoader.load(path_to_music)
        if self.sound:
            Clock.schedule_once(lambda dt: setattr(self.sound, 'volume', round(self.slider.value / 2000, 2)), 0.1)
            self.sound.play()

    def set_sound(self, instance, value):
        if self.sound:
            self.sound.volume = round(value / 2000, 2)


class MyApp(App):
    Config.set('graphics', 'width', '750')
    Config.set('graphics', 'height', '750')
    Config.write()
    load_dotenv()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.playlist = []
        self.db_path = getenv("DB_NAME")
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

        self.musicButton = Button(text="Моя музыка", font_size=1500 * 0.01)
        self.appButton = Button(text="Мои приложения", font_size=1500 * 0.01)
        self.layoutAppMusic = BoxLayout(orientation="horizontal", size_hint_y=0.03)
        self.mainLayout = BoxLayout(orientation='vertical', size=(Window.width, Window.height))
        self.secondMainLayout = GridLayout(cols=1, spacing=0, size_hint_y=None)
        self.scrollView = ScrollView()
        self.searchField = TextInput(
            multiline=False,
            font_size=1500 * 0.009,
            hint_text="Введите для поиска",
            size_hint_y=0.038,
        )
        self.soundPlay = SoundPlay()

        self.layoutAppMusic.add_widget(self.musicButton)
        self.layoutAppMusic.add_widget(self.appButton)
        self.mainLayout.add_widget(self.layoutAppMusic)
        self.mainLayout.add_widget(self.searchField)
        self.mainLayout.add_widget(self.scrollView)

    def search_music(self, instance, value):
        if value:
            musicList = list()
            for val in self.playlist:
                if val.children[1].text.lower().startswith(value.lower()):
                    musicList.append(val)
            self.secondMainLayout.clear_widgets()
            self.scrollView.clear_widgets()
            for music in musicList:
                self.secondMainLayout.add_widget(music)
            self.scrollView.add_widget(self.secondMainLayout)
        else:
            self.secondMainLayout.clear_widgets()
            self.scrollView.clear_widgets()
            for music in self.playlist:
                self.secondMainLayout.add_widget(music)
            self.scrollView.add_widget(self.secondMainLayout)

    def show_track(self, instance):
        self.secondMainLayout.clear_widgets()
        self.cur.execute(
            """
                select tr.Title, tr.RealId from T_PlaylistTrack plt
                left join T_Playlist pl on plt.Kind = pl.Kind
                left join T_Track tr on plt.TrackId = tr.RealId
                where pl.Kind = ?;
                """, (1015,)
        )

        for row in self.cur:
            musicToIdLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            music_ID = Label(text=str(row[1]), opacity=0, size_hint=(0, 0))
            music_name = Button(text=row[0], font_size=1500 * 0.01)
            music_name.bind(on_press=self.play_music)
            musicToIdLayout.add_widget(music_name)
            musicToIdLayout.add_widget(music_ID)
            self.secondMainLayout.add_widget(musicToIdLayout)
            self.playlist.append(musicToIdLayout)
        self.scrollView.clear_widgets()
        self.scrollView.add_widget(self.secondMainLayout)

    def play_music(self, instance):
        path_to_music = path.join(getenv("PATH_TO_MUSIC"), instance.parent.children[0].text + ".mp3")
        self.soundPlay.nameMusic.text = instance.text
        self.soundPlay.now_play = instance
        if self.soundPlay not in self.mainLayout.children:
            self.mainLayout.add_widget(self.soundPlay)
        if self.soundPlay.sound and self.soundPlay.sound.state == "play":
            self.soundPlay.sound.stop()
        self.soundPlay.load_sound(path_to_music)

    def build(self):
        Window.minimum_width = 750
        Window.minimum_height = 750
        self.secondMainLayout.bind(minimum_height=self.secondMainLayout.setter("height"))
        self.searchField.bind(text=self.search_music)
        self.musicButton.bind(on_press=self.show_track)
        return self.mainLayout


async def main():
    app = MyApp()
    await app.async_run()


if __name__ == "__main__":
    asyncio.run(main())
