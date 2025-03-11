# -- coding: utf-8
import json
from os import path
import requests


def func_weather() -> str:
    path_for_key = path.join('C:/Users/1/Desktop/tokens/tokens.json')

    with open(path_for_key, 'r') as file_token:
        TOKEN = json.load(file_token)['token_for_weather']


    CITY = 'Sevastopol, UA'
    CITY_ID = 694423
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': TOKEN})
        data = res.json()
        return "сегодня на улице " + data['weather'][0]['description'] + '. ' + "температура на улице " + data['main']['temp']
    except Exception as e:
        return 'Прости, но возникла ошибка'
