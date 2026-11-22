#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Образцы интерфейса Hades II (автор, 22.11.2026: «мне нравится интерфейс в Хейдес 2 — иконки, рамки и так далее»).
Кладёт в refs/screens/ui/hades2/:
  steam/NN.jpg  — кадры со страницы игры в Steam;
  site/         — кадр с сайта разработчика, которого нет в Steam;
  video/        — кадры из двух роликов со страницы Steam, где виден интерфейс (нужен ffmpeg);
  crops/        — крупные планы рамок и иконок, вырезанные из video/.
Вики игры (hades2.wiki.gg, hades.fandom.com) картинки скриптам не отдаёт — там проверка Cloudflare, её не обходим.
Запуск из корня репозитория: python3 -I refs/tools/fetch_hades2.py
Нужны Pillow и ffmpeg. Картинки чужие, в git не идут (refs/screens/ в .gitignore). Берём только подачу, не вещи и не героев."""
import io, json, os, site, subprocess, sys, time, urllib.request
sys.path.append(site.getusersitepackages())
from PIL import Image

OUT = os.environ.get("H2_OUT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "screens", "ui", "hades2")
APP = 1145350
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
SITE = ["https://images.ctfassets.net/5owu3y35gz1g/6Oocfxb7TB4kGyYf7Y4q4n/4f3b7f679be9300272bde56b48f28b37/hades2_apr30_05.jpg"]
TRAILER = "https://video.akamai.steamstatic.com/store_trailers/1145350/"
SHOW = TRAILER + "1078171228/d92eb59e06a0bc11acbab62a2fcc3981383b80fa/1758820310/hls_264_0_video.m3u8"  # v1.0 Showcase
EARLY = TRAILER + "695850/0b4a736847005fc3bf0110bb100cf8eb01fa20d1/1750627504/hls_264_0_video.m3u8"  # Early Access Showcase
# Кадры отбирались так: ролик целиком по кадру в 2 секунды (ss=None), а места с интерфейсом — гуще,
# по 3 кадра в секунду с отметки ss. Имя кадра: (ролик, ss, кадров в секунду, номер кадра с 1).
FRAMES = {
    "01_razgovor_zevs_zolotaya_rama": (EARLY, 42, 3, 8),
    "02_vybor_darov": (EARLY, 42, 3, 11),
    "03_razgovor_gekata": (SHOW, None, 0.5, 32),
    "04_razgovor_dora": (SHOW, None, 0.5, 45),
    "05_razgovor_selena": (SHOW, None, 0.5, 47),
    "06_razgovor_artemida": (SHOW, None, 0.5, 59),
    "07_arkana_rannyaya": (EARLY, 116, 3, 15),
    "08_arkana_vklyuchenie": (EARLY, 116, 3, 17),
    "09_arkana_1_0": (SHOW, 104, 3, 12),
    "10_arkana_1_0_vspyshka": (SHOW, 104, 3, 17),
    "11_klyatvy_plitki": (SHOW, 140, 3, 8),
    "12_ispytanie_rama_s_tsepyami": (SHOW, 140, 3, 13),
    "13_perekrestok_lavka": (SHOW, 120, 3, 11),
    "14_poloski_i_ikonki_v_boyu": (SHOW, 20, 3, 5),
    "15_vybor_puti": (SHOW, None, 0.5, 66),
}
# крупный план: (кадр, (лево, верх, право, низ) в точках кадра 1920×1080)
CROPS = {
    "a_zevs_rama": ("01_razgovor_zevs_zolotaya_rama", (540, 540, 1680, 1020)),
    "b_dary_stroki": ("02_vybor_darov", (395, 233, 1601, 973)),
    "c_dar_ikonka": ("02_vybor_darov", (395, 233, 560, 380)),
    "d_arkana_rannyaya_karty": ("07_arkana_rannyaya", (15, 8, 776, 971)),
    "e_arkana_karty": ("09_arkana_1_0", (85, 27, 645, 1011)),
    "f_arkana_bolshaya_karta": ("09_arkana_1_0", (840, 40, 1260, 640)),
    "g_klyatvy_plitki": ("11_klyatvy_plitki", (702, 176, 1474, 662)),
    "h_lavka_stroki": ("13_perekrestok_lavka", (57, 173, 871, 755)),
    "i_gekata_okno": ("03_razgovor_gekata", (634, 620, 1650, 1070)),
    "j_poloski": ("14_poloski_i_ikonki_v_boyu", (0, 860, 640, 1080)),
    "k_portret_v_koltse": ("07_arkana_rannyaya", (1442, 104, 1865, 527)),
    "l_vspyshka_karty": ("10_arkana_1_0_vspyshka", (78, 27, 670, 958)),
    "m_ispytanie_kartochki": ("12_ispytanie_rama_s_tsepyami", (600, 520, 1320, 960)),
    "n_ispytanie_zagolovok": ("12_ispytanie_rama_s_tsepyami", (420, 225, 1460, 400)),
}


def get(url, tries=3):
    for k in range(tries):  # Steam иногда рвёт связь, повторяем
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(3)


def save(raw, path):
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    im.thumbnail((1920, 1920))
    im.save(path, quality=88)


def main():
    for d in ("steam", "site", "video", "crops"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    meta = {"steam": f"https://store.steampowered.com/app/{APP}/", "frames": {}, "site": SITE}
    d = json.loads(get(f"https://store.steampowered.com/api/appdetails?appids={APP}&cc=US"))[str(APP)]["data"]
    for i, s in enumerate(d.get("screenshots", [])):
        p = os.path.join(OUT, "steam", f"{i + 1:02d}.jpg")
        if not os.path.exists(p):
            save(get(s["path_full"].split("?")[0]), p)
    for u in SITE:
        p = os.path.join(OUT, "site", u.rsplit("/", 1)[1])
        if not os.path.exists(p):
            save(get(u + "?w=1920"), p)
    for name, (video, ss, fps, n) in FRAMES.items():
        p = os.path.join(OUT, "video", name + ".jpg")
        if not os.path.exists(p):
            cmd = ["ffmpeg", "-loglevel", "error", "-y"] + (["-ss", str(ss)] if ss is not None else [])
            cmd += ["-i", video, "-vf", f"fps={fps},select=eq(n\\,{n - 1})", "-frames:v", "1", "-q:v", "2", p]
            for k in range(3):  # ролик идёт кусками по сети, кусок иногда не приходит — повторяем
                if subprocess.run(cmd).returncode == 0:
                    break
                time.sleep(3)
            else:
                raise RuntimeError("не вышел кадр " + name)
        meta["frames"][name] = {"video": "early_access_showcase" if video == EARLY else "v1_0_showcase",
                                "ss": ss, "fps": fps, "frame": n}
        print("кадр", name, flush=True)
    for name, (frame, box) in CROPS.items():
        Image.open(os.path.join(OUT, "video", frame + ".jpg")).crop(box).save(
            os.path.join(OUT, "crops", name + ".jpg"), quality=90)
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("готово")


if __name__ == "__main__":
    main()
