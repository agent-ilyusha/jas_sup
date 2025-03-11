# -- coding: utf-8
import json
import queue
from typing import Any

import vosk
import sys
import sounddevice as sd

import torch_iter

from fuzzywuzzy import fuzz
from os import path
from vosk import Model

from modules import anekdot, browser, module_time, start_app, weather


class Speech:
    def __init__(self):
        self.q = queue.Queue()
        self.FRAME_RATE = 16000
        self.CHANNELS = 1
        self.MODEL = Model("model-0.22")
        self.DEVICE = 0
        self.path_for_json_files = path.join('C:/Users/1/Desktop/my_support/json_files/command_json.json')

    def callback(self, indata, frames, time, status):
        """
        Set framerate.
        :param indata:
        :param frames:
        :param time:
        :param status:
        :return:
        """
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))


    def del_command_word(self, txt: str, pfjf: str):
        """
        Remove unnecessary words.
        :param txt:
        :param pfjf: Project file json format - file in which words are stored.
        :return: Cleaned up text.
        """
        with open(pfjf, encoding='utf-8') as file_command:
            command_list = json.load(file_command)['command_word']
            txt_list = txt.split()
            new_txt = list()
            for el in txt_list:
                if el not in (command_list or self.accelerating_words):
                    new_txt.append(el)
            return ' '.join(new_txt)

    def accelerating_words(self) -> set[Any]:
        with open(self.path_for_json_files, encoding='utf-8') as file:
            var = json.load(file)
            words = set(var['accelerating_words'])
            answer_comm = var['answer_bot']
        return words


    def sound_pad(self) -> str:
        """
        Managing assistant commands.
        :return: Text for speaking.
        """
        with sd.RawInputStream(samplerate=self.FRAME_RATE,
                               blocksize=8000,
                               device=self.DEVICE,
                               dtype='int16',
                               channels=1,
                               callback=self.callback):

            rec = vosk.KaldiRecognizer(self.MODEL, self.FRAME_RATE)
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    value = rec.FinalResult()
                    print(json.loads(value)['text'])
                    clearedLine = self.del_command_word(json.loads(value)['text'], self.path_for_json_files)

                    if set(json.loads(value)['text'].split()).intersection(self.accelerating_words()):
                        torch_iter.torch_func('сделаю все возможное')
                    if fuzz.ratio('время' == clearedLine) >= 75:
                        return module_time.time_func()
                    elif fuzz.ratio('дату' == clearedLine) >= 75:
                        return module_time.data_func()
                    elif fuzz.ratio('запустизапусти' == clearedLine) >= 75:
                        del_word = self.del_command_word(json.loads(value)['text'], self.path_for_json_files)
                        return start_app.func_cycle(del_word)
                    elif fuzz.ratio('анекдот' == clearedLine) >= 75:
                        return anekdot.return_anekdot()
                    elif fuzz.ratio('браузер' == clearedLine) >= 75:
                        del_word = self.del_command_word(json.loads(value)['text'], self.path_for_json_files)
                        return browser.search_func(del_word)
                    elif fuzz.ratio('погода' == clearedLine) >= 75:
                        return weather.func_weather()
                    else:
                        return 'Скажи еще раз и внятно, пожалуйста'
