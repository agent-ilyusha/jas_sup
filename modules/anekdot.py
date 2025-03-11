# -- coding: utf-8
import requests
import random
import bs4



def return_anekdot() -> str:
    page_num = random.randint(0, 2021)
    page = f'http://bashorg.org/page/{page_num}/'
    json_page = requests.get(page).text
    soup = bs4.BeautifulSoup(json_page, "lxml")
    llist = list()

    for el in soup.find_all():
        str_el = str(el)
        if str_el.startswith('<div class="quote">'):
            llist.append(str_el[len('<div class="quote">'):len(str_el)-len(' </div>')].replace('<br/>', ' '))

    return llist[random.randint(0, len(llist))]



