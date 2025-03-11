# -- coding: utf-8
import torch
import time
import sounddevice as sd


def torch_func(txt):
    language = 'ru'
    model_id = 'v3_1_ru'
    sample_rate = 48000
    speaker = 'baya'  # aidar, baya, kseniya, xenia, random
    put_accent = True
    put_yo = True
    device = torch.device('cpu')
    text = txt


    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                         model='silero_tts',
                                         language=language,
                                         speaker=model_id)

    model.to(device)
    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio)
    time.sleep(len(audio)/sample_rate+0.3)
    sd.stop()
