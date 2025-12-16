from PIL import Image

image = Image.open("SnowOwl2.jpg")
raster = image.load()
W, H = image.size

integral = [[0]*W for _ in range(H)]

def gray(px):
    if isinstance(px, int): 
        return px
    r, g, b = px[0], px[1], px[2]
    return int(0.299*r + 0.587*g + 0.114*b)

for y in range(H):
    for x in range(W):
        g = gray(raster[x, y])
        a = integral[y][x-1] if x > 0 else 0
        b = integral[y-1][x] if y > 0 else 0
        c = integral[y-1][x-1] if x > 0 and y > 0 else 0
        integral[y][x] = g + a + b - c

def b_avg(x0, y0, x1, y1):
    A = (x1-x0) * (y1-y0)
    s1 = integral[y1-1][x1-1]
    s2 = integral[y0-1][x1-1] if y0 > 0 else 0
    s3 = integral[y1-1][x0-1] if x0 > 0 else 0
    s4 = integral[y0-1][x0-1] if x0 > 0 and y0 > 0 else 0
    total = s1 - s2 - s3 + s4
    return total // A

block = 16
out = Image.new("L", (W, H))
put = out.putpixel

for by in range(0, H, block):
    for bx in range(0, W, block):
        x0 = bx
        y0 = by
        x1 = min(bx + block, W)
        y1 = min(by + block, H)
        avg = b_avg(x0, y0, x1, y1)
        for y in range(y0, y1):
            for x in range(x0, x1):
                put((x, y), avg)

out.save("p_integral128.png")
