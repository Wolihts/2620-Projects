from PIL import Image
import random

block   = 128
sample = 64
seed    = 42

def clmp(v):
    if v < 0: return 0
    if v > 255: return 255
    return int(v)

def vpixel(px):
    if isinstance(px, int):
        return (int(px),)
    if len(px) >= 3:
        return (int(px[0]), int(px[1]), int(px[2]))
    return (int(px[0]),)

def pixelv(vec, channels):
    if channels == 1:
        return clmp(vec[0])
    return tuple(clmp(v) for v in vec[:channels])

def dist2(a, b):
    n = min(len(a), len(b))
    s = 0
    for i in range(n):
        d = int(a[i]) - int(b[i])
        s += d*d
    return s

if seed is not None:
    random.seed(seed)

image = Image.open("SnowOwl.jpg")
raster = image.load()
W, H = image.size

sample_px = raster[0, 0]
sample_vec = vpixel(sample_px)
C = len(sample_vec)

output = Image.new(image.mode, (W, H))
out_raster = output.load()

for by in range(0, H, block):
    for bx in range(0, W, block):
        x0 = bx
        y0 = by
        x1 = min(bx + block, W)
        y1 = min(by + block, H)
        sum_vec = [0.0]*C
        count = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                v = vpixel(raster[x, y])
                for i in range(C):
                    sum_vec[i] += v[i]
                count += 1

        if count == 0:
            avg_vec = [0.0]*C
        else:
            avg_vec = [sum_vec[i]/count for i in range(C)]
        target = tuple(avg_vec)
        n_w = x1 - x0
        n_h = y1 - y0
        total_pixels = n_w * n_h
        if sample >= total_pixels:
            positions = [(x, y) for y in range(y0, y1) for x in range(x0, x1)]
        else:
            positions = []
            for _ in range(sample):
                rx = random.randint(x0, x1-1)
                ry = random.randint(y0, y1-1)
                positions.append((rx, ry))
        best_px = None
        best_d2 = None
        for (px_x, px_y) in positions:
            px_val = raster[px_x, px_y]
            vec = vpixel(px_val)
            d2 = dist2(vec, target)
            if best_d2 is None or d2 < best_d2:
                best_d2 = d2
                best_px = px_val
        if best_px is None:
            best_px = pixelv(target, C)
        for y in range(y0, y1):
            for x in range(x0, x1):
                out_raster[x, y] = best_px

output.save("p_kmedoid128.png")
