from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageDraw
from PIL import ImageOps
from imager2 import Imager

def left(bilde):
    bild = Imager(bilde)
    #bild = bild.resize(1000, 1000)
    width, height = bild.image.size
    #bild.display()
    left = 0
    top = 0
    right = width/2
    bot = height
    bild.image = bild.image.crop((left, top, right, bot))
    return bild

def right(bilde):
    bild = Imager(bilde)
    #bild = bild.resize(1000, 1000)
    width, height = bild.image.size
    # bild.display()
    left = width/2
    top = 0
    right = width
    bot = height
    bild.image = bild.image.crop((left, top, right, bot))
    return bild

def count_color(color, image):
    rgb = 0
    if color == "red":
        rgb = 0
    elif color == "green":
        rgb = 1
    elif color == "blue":
        rgb = 2

    tall = 0
    num = image.image.convert("RGB").getcolors(10000)
    print(max(num))
    for i in num:
        if i[1][rgb]>100:
            tall += i[0]
    return tall

if __name__ == '__main__':

    b = left("C:/Users/Runar AJ/Dropbox/Skole/ProglabV2/Oppgave5/test.gif")
    b.display()
    r = right("C:/Users/Runar AJ/Dropbox/Skole/ProglabV2/Oppgave5/test.gif")
    r.display()
    num = r.image.getcolors(maxcolors=100000)
    tall = 0
    for i in num:
        if i[1][1]>50:
            tall += i[0]

    print(tall)
    num2 = b.image.convert("RGB").getcolors(maxcolors=100000)
    tall2 = 0
    for j in num2:
        if j[1][1]>240:
            tall2 += j[0]
    print(tall2)

