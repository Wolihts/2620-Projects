from PIL import Image
import random
import math

def l2_difference(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def closest_color(color, color_list):
    return min(color_list, key=lambda option: l2_difference(color, option))

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

image = Image.open("cheetah.jpg")
raster = image.load()

color_count = dict()
for y in range(image.height):
    for x in range(image.width):
        px = raster[x, y]
        if isinstance(px, int):
            pixel = (px, px, px)
        else:
            if len(px) >= 3:
                pixel = (px[0], px[1], px[2])
            else:
                v = px[0]
                pixel = (v, v, v)
        if pixel not in color_count:
            color_count[pixel] = 0
        color_count[pixel] += 1

sorted_color_count = sorted(color_count.items(), key=lambda item: item[1], reverse=True)

k = 12
iterations = 1
palette = [random_color() for _ in range(k)]

for i in range(iterations):
    clusters = [[] for _ in range(k)]

    for color, count in sorted_color_count:
        c = closest_color(color, palette)
        idx = palette.index(c)
        clusters[idx].append((color, count))

    for j in range(k):
        cluster = clusters[j]
        if len(cluster) == 0:
            palette[j] = random_color()
        else:
            sums = [0, 0, 0]
            total_weight = 0
            for color, count in cluster:
                sums[0] += color[0] * count
                sums[1] += color[1] * count
                sums[2] += color[2] * count
                total_weight += count
            palette[j] = (
                sums[0] // total_weight,
                sums[1] // total_weight,
                sums[2] // total_weight
            )

for y in range(image.height):
    for x in range(image.width):
        px = raster[x, y]
        if isinstance(px, int):
            pixel = (px, px, px)
        else:
            if len(px) >= 3:
                pixel = (px[0], px[1], px[2])
            else:
                v = px[0]
                pixel = (v, v, v)
        raster[x, y] = closest_color(pixel, palette)

image.save("posterized8.png")
