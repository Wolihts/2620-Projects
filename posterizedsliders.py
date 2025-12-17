from PIL import Image
import random

# I did not add image.open or image.save so that this function can be imported and used elsewhere
# image = Image.open("test.jpg")
#use example in Index.py for how to call this function and save the result


def l2_difference(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def to3(px):
    if isinstance(px, int):
        v = int(px)
        return (v, v, v)
    if len(px) >= 3:
        return (int(px[0]), int(px[1]), int(px[2]))
    v = int(px[0])
    return (v, v, v)

def closest_index(color, palette):
    best_i = 0
    best_d = None
    for i, c in enumerate(palette):
        d = l2_difference(color, c)
        if best_d is None or d < best_d:
            best_d = d
            best_i = i
    return best_i

def posterize(image, k=2, iterations=1, top_colors=20000):
    img = image.copy()
    r = img.load()
    w, h = img.size

    color_count = {}
    for y in range(h):
        for x in range(w):
            p = to3(r[x, y])
            color_count[p] = color_count.get(p, 0) + 1

    items = sorted(color_count.items(), key=lambda it: it[1], reverse=True)
    train = items[:min(len(items), top_colors)]

    palette = [random_color() for _ in range(k)]

    for _ in range(iterations):
        clusters = [[] for _ in range(k)]
        for color, count in train:
            idx = closest_index(color, palette)
            clusters[idx].append((color, count))

        for j in range(k):
            cluster = clusters[j]
            if not cluster:
                palette[j] = random_color()
            else:
                s0 = s1 = s2 = 0
                tw = 0
                for color, count in cluster:
                    s0 += color[0] * count
                    s1 += color[1] * count
                    s2 += color[2] * count
                    tw += count
                palette[j] = (s0 // tw, s1 // tw, s2 // tw)

    for y in range(h):
        for x in range(w):
            px = r[x, y]
            c3 = to3(px)
            idx = closest_index(c3, palette)
            new = palette[idx]
            if isinstance(px, int):
                r[x, y] = new[0]
            else:
                if len(px) >= 3:
                    r[x, y] = new[:len(px)]
                else:
                    r[x, y] = (new[0],)

    return img

