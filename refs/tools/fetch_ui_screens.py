#!/usr/bin/env python3
"""Скачивает скриншоты игр с сильным интерфейсом (образцы для нашего UI)
в refs/screens/ui/<игра>/NN.jpg и пишет refs/screens/ui/meta.json.
Запуск из корня репозитория: python3 -I refs/tools/fetch_ui_screens.py
Нужен Pillow. Скриншоты чужие, в git не идут (см. .gitignore)."""
import io, json, os, site, sys, time, urllib.request
sys.path.append(site.getusersitepackages())
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "screens", "ui")
MAX = 12  # интерфейс бывает виден не на первых кадрах, поэтому берём больше

STEAM = {
    # мультяшный контур и плотный цвет, «толстый» интерфейс
    "kingdom_rush_5": 2849080, "kingdom_rush_vengeance": 1367550, "legends_of_kingdom_rush": 1904860,
    "castle_crashers": 204360, "pit_people": 291860, "nobody_saves_the_world": 1432050,
    "cult_of_the_lamb": 1313140, "rogue_legacy_2": 1253920, "pvz": 3590, "shop_titans": 1258080,
    "going_under": 1154810, "thank_goodness": 2366980, "lil_guardsman": 1924360, "bear_and_breakfast": 1136370,
    # карты как вещи
    "wildfrost": 1811990, "floppy_knights": 1057800, "dicey_dungeons": 861540, "slay_the_spire_2": 2868840,
    "monster_train_2": 2742830, "balatro": 2379780, "griftlands": 601840, "roguebook": 1076200,
    "krumits_tale": 1073320, "stacklands": 1948280, "cardpocalypse": 904400, "voice_of_cards": 1113570,
    "night_of_full_moon": 2592550, "dungeon_clawler": 2356780, "backpack_hero": 1970580,
    # текст, выборы и книга
    "potionomics": 1874490, "monster_prom": 743450, "exocolonist": 1148760, "beacon_pines": 1269640,
    "plucky_squire": 1627570, "wytchwood": 729000, "storyteller": 1624540, "yes_your_grace_2": 1373090,
    "later_alligator": 966320, "spiritfarer": 972660, "cozy_grove": 1458100, "hades": 1145360,
    "oxygen_not_included": 457140, "root": 965580, "armello": 290340, "dave_the_diver": 1868140,
}
ITUNES = {"hearthstone": 625257520, "clash_royale": 1053012308}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()


def save(raw, path):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    im.thumbnail((1280, 1280))
    im.save(path, quality=82)


def main():
    os.makedirs(OUT, exist_ok=True)
    mp = os.path.join(OUT, "meta.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    for key, appid in STEAM.items():
        if key in meta and os.path.isdir(os.path.join(OUT, key)):
            continue
        try:
            d = json.loads(get(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=russian&cc=US"))[str(appid)]
        except Exception as e:
            print(key, "ошибка", e); time.sleep(3); continue
        if not d.get("success"):
            print(key, "не найдено"); continue
        d = d["data"]
        os.makedirs(os.path.join(OUT, key), exist_ok=True)
        shots = d.get("screenshots", [])
        n = 0
        for i, s in enumerate(shots[:MAX]):
            p = os.path.join(OUT, key, f"{i+1:02d}.jpg")
            try:
                if not os.path.exists(p):
                    save(get(s["path_full"].split("?")[0]), p)
                n += 1
            except Exception as e:
                print(key, i, "ошибка", e)
        meta[key] = {"appid": appid, "name": d["name"], "release": d.get("release_date", {}).get("date"),
                     "dev": d.get("developers"), "url": f"https://store.steampowered.com/app/{appid}/", "shots": n}
        json.dump(meta, open(mp, "w"), ensure_ascii=False, indent=1)
        print(key, d["name"], n, flush=True); time.sleep(1.3)
    for key, tid in ITUNES.items():
        if key in meta:
            continue
        try:
            r = json.loads(get(f"https://itunes.apple.com/lookup?id={tid}&country=us"))["results"][0]
        except Exception as e:
            print(key, "ошибка", e); continue
        os.makedirs(os.path.join(OUT, key), exist_ok=True)
        urls = (r.get("ipadScreenshotUrls") or r.get("screenshotUrls") or [])[:MAX]
        n = 0
        for i, u in enumerate(urls):
            try:
                # в конце адреса стоит размер; просим покрупнее
                big = u.rsplit("/", 1)[0] + "/1600x1600bb.jpg"
                save(get(big), os.path.join(OUT, key, f"{i+1:02d}.jpg")); n += 1
            except Exception as e:
                print(key, i, "ошибка", e)
        meta[key] = {"itunes": tid, "name": r.get("trackName"), "dev": [r.get("artistName")],
                     "url": r.get("trackViewUrl", "").split("?")[0], "shots": n}
        json.dump(meta, open(mp, "w"), ensure_ascii=False, indent=1)
        print(key, r.get("trackName"), n, flush=True)


if __name__ == "__main__":
    main()
