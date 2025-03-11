# -- coding: utf-8

import asyncio
import sqlite3

from dotenv import load_dotenv
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config

from MyKivyClass.musicBox import MusicBox
from MyKivyClass.soundPlay import SoundPlay


class MyApp(App):
    Config.set('graphics', 'width', '750')
    Config.set('graphics', 'height', '750')
    Config.write()
    load_dotenv()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.musicButton = Button(text="Моя музыка", font_size=1500 * 0.01)
        self.appButton = Button(text="Мои приложения", font_size=1500 * 0.01)
        self.layoutAppMusic = BoxLayout(orientation="horizontal", size_hint_y=0.03)
        self.mainLayout = BoxLayout(orientation='vertical', size=(Window.width, Window.height))
        self.soundPlay = SoundPlay()
        self.musicBox = MusicBox()
        self.searchField = TextInput(
            multiline=False,
            font_size=1500 * 0.009,
            hint_text="Введите для поиска",
            size_hint_y=0.038,
        )

        self.layoutAppMusic.add_widget(self.musicButton)
        self.layoutAppMusic.add_widget(self.appButton)
        self.mainLayout.add_widget(self.layoutAppMusic)
        self.mainLayout.add_widget(self.searchField)
        self.mainLayout.add_widget(self.musicBox)

    def build(self):
        Window.minimum_width = 750
        Window.minimum_height = 750
        self.musicButton.bind(on_press=self.musicBox.show_track)
        self.searchField.bind(text=self.musicBox.search_music)
        return self.mainLayout


async def main():
    app = MyApp()
    await app.async_run()


if __name__ == "__main__":
    asyncio.run(main())
