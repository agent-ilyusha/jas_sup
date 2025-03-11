# -- coding: utf-8
import time
import num2words as nw
import json


def data_func() -> str:
    global dict_month, KEY
    now_time = time.gmtime()
    year = nw.num2words(number=now_time.tm_year, lang='ru')
    day = nw.num2words(number=now_time.tm_mday, lang='ru')
    return f'сейчас {year} год; ' \
           f'месяц {dict_month[now_time.tm_mon]}; ' \
           f'день {day};'


def time_func() -> str:
    now_time = time.gmtime()
    hour = nw.num2words(number=now_time.tm_hour+3, lang='ru')
    minute = nw.num2words(number=now_time.tm_min, lang='ru')
    return f'сейчас {hour} часов, {minute} минут'


dict_month = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май',
              6: 'июнь', 7: 'июль', 8: 'август', 9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}
KEY = 'ru'

#
