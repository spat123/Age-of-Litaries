from PIL import Image
from collections import deque
from pathlib import Path

SRC = Path(r"C:\Users\Игорь\.cursor\projects\f-Age-of-Litaries\assets")
DST = Path(r"F:\Age of Litaries\game\assets\art\icons")
DST.mkdir(parents=True, exist_ok=True)

NAMES = [
	"icon_health",
	"icon_mental",
	"icon_gold",
	"icon_crown",
	"icon_inquisition",
	"icon_people",
	"icon_cringe",
]


def is_bg(r: int, g: int, b: int) -> bool:
	lum = (r + g + b) / 3.0
	mx, mn = max(r, g, b), min(r, g, b)
	sat = mx - mn
	# magenta / fuchsia chroma key
	if r > 180 and b > 180 and g < 140 and (r - g) > 40 and (b - g) > 40:
		return True
	if r > 200 and b > 150 and g < 160 and sat > 80 and abs(r - b) < 80:
		return True
	# cream parchment
	if lum >= 165 and sat <= 85:
		return True
	if r >= 185 and g >= 165 and b >= 120 and sat <= 100 and lum >= 155:
		return True
	if r >= 200 and g >= 180 and b >= 140 and (r - b) <= 90 and sat <= 110:
		return True
	# wood frame
	if lum <= 95 and sat <= 55:
		return True
	if 25 <= lum <= 115 and sat <= 48 and r >= g - 5:
		return True
	return False


def remove_bg(im: Image.Image) -> Image.Image:
	im = im.convert("RGBA")
	w, h = im.size
	px = im.load()
	visited = [[False] * h for _ in range(w)]
	q: deque = deque()

	def seed(x: int, y: int) -> None:
		if 0 <= x < w and 0 <= y < h and not visited[x][y]:
			r, g, b, a = px[x, y]
			if a > 0 and is_bg(r, g, b):
				q.append((x, y))
				visited[x][y] = True

	for x in range(w):
		seed(x, 0)
		seed(x, h - 1)
	for y in range(h):
		seed(0, y)
		seed(w - 1, y)

	while q:
		x, y = q.popleft()
		r, g, b, _a = px[x, y]
		px[x, y] = (r, g, b, 0)
		for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
			if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny]:
				visited[nx][ny] = True
				rr, gg, bb, aa = px[nx, ny]
				if aa > 0 and is_bg(rr, gg, bb):
					q.append((nx, ny))

	for y in range(h):
		for x in range(w):
			r, g, b, a = px[x, y]
			if a == 0:
				continue
			if is_bg(r, g, b):
				for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
					if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
						px[x, y] = (r, g, b, 0)
						break

	# remove magenta fringe near transparency
	for y in range(h):
		for x in range(w):
			r, g, b, a = px[x, y]
			if a == 0:
				continue
			if r > 160 and b > 140 and g < 150 and (r - g) > 25:
				near_t = False
				for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
					if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0:
						near_t = True
						break
				if near_t:
					px[x, y] = (r, g, b, 0)

	bbox = im.getbbox()
	if bbox:
		pad = 6
		l, t, r, b = bbox
		im = im.crop((max(0, l - pad), max(0, t - pad), min(w, r + pad), min(h, b + pad)))

	im.thumbnail((256, 256), Image.Resampling.LANCZOS)
	canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
	canvas.paste(im, ((256 - im.width) // 2, (256 - im.height) // 2), im)
	return canvas


def main() -> None:
	for name in NAMES:
		src = SRC / f"{name}_raw.png"
		if not src.exists():
			print("MISSING", src)
			continue
		out = remove_bg(Image.open(src))
		out.save(DST / f"{name}.png", "PNG")
		out.save(SRC / f"{name}.png", "PNG")
		opaque = sum(1 for p in out.getdata() if p[3] > 0)
		print(name, "corner", out.getpixel((0, 0)), "opaque", opaque)
	print("done")


if __name__ == "__main__":
	main()
