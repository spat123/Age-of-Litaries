#!/usr/bin/env python3
"""Убирает жёлтый налёт с картинки: выравнивает баланс белого, остужает тени, чуть снижает насыщенность.
Запуск: python3 web/tools/fix_yellow.py вход.png выход.webp [ширина]
Печатает «жёлтость» до и после. У старых фонов игры она в среднем около 20, выше 50 — заметно желтит."""
import sys
import numpy as np
from PIL import Image

def yellowness(img):
    s = np.asarray(img.convert("RGB").resize((160, 90))).astype(float)
    r, g, b = s[..., 0], s[..., 1], s[..., 2]
    return ((r + g) / 2 - b).mean()

def fix(img, gains=(0.94, 1.0, 1.26), shadow=(-0.05, 0.0, 0.10), desat=0.12):
    x = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    x = x * np.array(gains, dtype=np.float32)
    luma = (0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2])[..., None]
    x = x + np.clip(1.0 - luma, 0, 1) ** 1.6 * np.array(shadow, dtype=np.float32)
    luma = (0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2])[..., None]
    x = luma + (x - luma) * (1 - desat)
    return Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8))

if __name__ == "__main__":
    src = Image.open(sys.argv[1])
    out = fix(src)
    if len(sys.argv) > 3:
        w = int(sys.argv[3])
        out = out.resize((w, round(out.height * w / out.width)), Image.LANCZOS)
    out.save(sys.argv[2], quality=88)
    print(f"жёлтость: было {yellowness(src):.0f}, стало {yellowness(out):.0f}")
