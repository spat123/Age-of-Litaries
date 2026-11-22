#!/usr/bin/env python3
"""Скачивает скриншоты игр-образцов со страниц Steam (и Sort the Court с itch.io)
в refs/screens/<игра>/NN.jpg и пишет refs/screens/meta.json.
Запуск из корня репозитория: python3 refs/tools/fetch_screens.py
Нужен Pillow. Скриншоты чужие, в git не идут (см. .gitignore)."""
import io, json, os, time, urllib.request
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "screens")
STEAM = {
    "col_middle_ages": 1337890, "col_middle_ages_2": 1573630, "col_wild_islands": 2380320,
    "col_modern_ages": 3049140, "col_samosbor": 1574570,
    "reigns": 474750, "reigns_three_kingdoms": 2437040, "sir_brante": 1272160,
    "yes_your_grace": 1115690, "king_of_the_castle": 1839880, "cultist_simulator": 718670,
    "chinese_parents": 736190, "growing_up": 1191120, "the_yawhg": 269030,
    "death_and_taxes": 1166290, "slay_the_princess": 1989270, "wildermyth": 763890,
    "pentiment": 1205520, "inkulinati": 957960, "astrologaster": 742520,
    "procession_to_calvary": 1071130, "pilgrims": 1049280, "card_shark": 1371720,
    "foretales": 1170080,
    # смежные игры с близкой манерой рисунка
    "creaks": 956030, "machinarium": 40700, "potion_craft": 1210320,
    "tails_of_iron": 1283410, "dont_starve": 219740,
}
ITCH = {  # страница https://graebor.itch.io/sort-the-court
    "sort_the_court": [
        "https://img.itch.zone/aW1hZ2UvNDczNjcvMjA1ODYxLnBuZw==/original/EMzfdv.png",
        "https://img.itch.zone/aW1hZ2UvNDczNjcvMjA1ODYyLnBuZw==/original/Zb0%2FSF.png",
        "https://img.itch.zone/aW1hZ2UvNDczNjcvMjA1ODYzLnBuZw==/original/uGzgBU.png",
    ],
}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()

def save(raw, path):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    im.thumbnail((1280, 1280))
    im.save(path, quality=82)

meta = {}
for key, appid in STEAM.items():
    d = json.loads(get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=russian&cc=US"))[str(appid)]
    if not d.get("success"):
        print(key, "не найдено"); continue
    d = d["data"]
    os.makedirs(os.path.join(OUT, key), exist_ok=True)
    shots = d.get("screenshots", [])
    for i, s in enumerate(shots[:8]):
        p = os.path.join(OUT, key, f"{i+1:02d}.jpg")
        if not os.path.exists(p):
            save(get(s["path_full"].split("?")[0]), p)
    meta[key] = {"appid": appid, "name": d["name"], "release": d.get("release_date", {}).get("date"),
                 "dev": d.get("developers"), "short": d.get("short_description"),
                 "url": f"https://store.steampowered.com/app/{appid}/"}
    print(key, d["name"], len(shots)); time.sleep(1.2)
for key, urls in ITCH.items():
    os.makedirs(os.path.join(OUT, key), exist_ok=True)
    for i, u in enumerate(urls):
        save(get(u), os.path.join(OUT, key, f"{i+1:02d}.jpg"))
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), ensure_ascii=False, indent=1)
