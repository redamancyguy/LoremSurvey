import os
import random
from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw


def generate_code():
    source = '0123456789qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
    code = ''
    for i in range(4):
        code += random.choice(source)
    return code

import base64
def getCAPTCHA(request):
    mode = "RGB"  # 颜色模式
    size = (200, 100)  # 画布大小

    red = random.randrange(255)
    green = random.randrange(255)
    blue = random.randrange(255)
    color_bg = (red, green, blue)  # 背景色

    image = Image.new(mode=mode, size=size, color=color_bg)  # 画布
    imagedraw = ImageDraw(image, mode=mode)  # 画笔
    verify_code = generate_code()  # 内容
    print(os.getcwd())
    imagefont = ImageFont.truetype(os.getcwd() + '/../files/Roboto-Regular.ttf', 100)
    # 字体 颜色
    for i in range(len(verify_code)):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        imagedraw.text(xy=(50 * i, 0), text=verify_code[i], fill=fill, font=imagefont)
    # 噪点
    for i in range(1000):
        fill = (random.randrange(255), random.randrange(255), random.randrange(255))
        xy = (random.randrange(201), random.randrange(100))
        imagedraw.point(xy=xy, fill=fill)
    fp = BytesIO()
    image.save(fp, 'png')
    image.show()
    fp.getvalue()


getCAPTCHA("")