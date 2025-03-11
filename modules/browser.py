# -- coding: utf-8
import webbrowser
from fuzzywuzzy import fuzz


def search_func(txt: str) -> str:
    insert = txt.replace(' ', '+')
    webbrowser.open_new(f'https://yandex.fr/search/?text={insert}&lr=959')
    return 'Обработала твой запрос'


def open_vk():
    webbrowser.open_new(f'https://vk.com/im')
    return 'Готово'
