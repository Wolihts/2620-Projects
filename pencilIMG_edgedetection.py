from PIL import Image
import math

image = Image.open("owl.jpg")
raster = image.load()
W, H = image.size

gray = [[0]*W for _ in range(H)]

for y in range(H):
    for x in range(W):
        px = raster[x, y]
        if isinstance(px, int):
            g = px
        else:
            if len(px) >= 3:
                r, g0, b = px[0], px[1], px[2]
                g = int(0.299*r + 0.587*g0 + 0.114*b)
            else:
                g = int(px[0])
        gray[y][x] = g

out = Image.new("L", (W, H))
out_raster = out.load()

for y in range(H):
    for x in range(W):
        out_raster[x, y] = 255

for y in range(1, H-1):
    for x in range(1, W-1):
        gx = gray[y][x+1] - gray[y][x-1]
        gy = gray[y+1][x] - gray[y-1][x]
        mag = abs(gx) + abs(gy)
        if mag > 255:
            mag = 255
        val = 255 - mag
        out_raster[x, y] = val

out.save("pencil_owl.png")
