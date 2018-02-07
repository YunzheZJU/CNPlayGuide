# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image
import pytesser
import re


def ocr():
    print "OCR..."
    # 二值化初始化
    threshold = 127
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 替换表初始化
    rep = {
        'A': '6',
        'E': '6',
        'I': '1',
        'O': '0',
        'S': '8',
        '£': '8'
    }
    rgb = Image.open('img.gif').convert('RGB')
    for x in range(200):
        for y in range(30):
            (r, g, b) = rgb.getpixel((x, y))
            if r in (51, 102, 153, 204, 255) \
                    and g in (43, 85, 128, 170, 213, 255) \
                    and b in (51, 102, 153, 204, 255):
                rgb.putpixel((x, y), (255, 255, 255))
    rgb = rgb.convert('L').point(table, '1')
    # rgb.show()
    code = pytesser.image_to_string(rgb)
    result = ''
    for words in code.splitlines():
        result += words
    result = ''.join(result.split()).upper()
    for r in rep:
        result = result.replace(r, rep[r])
    result = filter(str.isdigit, result)
    reg = r'^(\d{6})$'
    try:
        result = re.match(reg, result).group(1)
    except:
        print "Error occurred in OCR."
        rgb.close()
        return "Error"
    rgb.close()
    return result
