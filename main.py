# --coding: utf-8
import json
import random
import speech

import torch_iter

from dotenv import load_dotenv
from os import path, getenv

load_dotenv()


def start_app() -> None:

    path_for_json_files = path.join(getenv("COMMAND_JSON"))
    with open(path_for_json_files, encoding='utf-8') as file:
        var = json.load(file)
        list_my_name = var['my_name']
        list_answer = var['answer_bot']

    torch_iter.torch_func(f'Привет,{random.choice(list_my_name)}')
    while True:
        speech_definition = speech.Speech()
        torch_iter.torch_func(speech_definition.sound_pad())


if __name__ == '__main__':
    start_app()
