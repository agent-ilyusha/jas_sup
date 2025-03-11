# -- coding: utf-8
import sqlite3
from os import getenv, path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from modules.MyKivyClass.soundPlay import SoundPlay


class MusicBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.playlist = []
        self.db_path = getenv("DB_NAME")
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

        self.secondMainLayout = GridLayout(cols=1, spacing=0, size_hint_y=None)
        self.scrollView = ScrollView()
        self.soundPlay = SoundPlay()
        self.secondMainLayout.bind(minimum_height=self.secondMainLayout.setter("height"))

        self.add_widget(self.scrollView)

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
        if self.soundPlay not in self.children:
            self.add_widget(self.soundPlay)
        if self.soundPlay.sound and self.soundPlay.sound.state == "play":
            self.soundPlay.sound.stop()
        self.soundPlay.load_sound(path_to_music)
