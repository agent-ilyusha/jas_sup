# -- coding: utf-8
from os import path, getenv

from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider


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
