# -- coding: utf-8

import sqlite3

from dotenv import load_dotenv
from fuzzywuzzy import fuzz
from os import getenv

load_dotenv()


def start_music(name: str) -> str:
    db_name = getenv("DB_NAME")
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("select * from T_Track tr where tr.Title like ?", (name.capitalize(), ))

    for row in cur:
        print(row)

    conn.close()


def start_playlist(name: str) -> str:
    db_name = getenv("DB_NAME")
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("select Kind, Title from T_Playlist")


    if fuzz.ratio("Скачанные треки", name) >= 75 or fuzz.ratio("Скачанная музыка", name) >= 75:
        name_playlist = "Downloaded tracks"
    elif fuzz.ratio("Мои любимые", name) >= 75 or fuzz.ratio("Любимые", name) >= 75:
        name_playlist = "Favorites"
    else:
        name_playlist = name

    for row in cur:
        if fuzz.ratio(row[1].lower(), name_playlist.lower()) >= 85:
            name_playlist = row
            break
    else:
        return "Такого плейлиста нет"

    cur.execute("""
    select tr.Title, tr.RealId from T_PlaylistTrack plt
    left join T_Playlist pl on plt.Kind = pl.Kind
    left join T_Track tr on plt.TrackId = tr.RealId
    where pl.Kind = ?;""", (name_playlist[0],)
    )
    for row in cur:
        print(row)

    conn.close()
    return name_playlist


print(start_playlist("орео"))
