# -*- coding: utf-8 -*-
# OCR测试 识别率：63 in 89 正确率：31 in 63
try:
    import Image
except ImportError:
    from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import pytesser
import re

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
for i in range(1, 90):
    filename = 'img/img%s.gif' % i
    image = Image.open(filename)
    rgb = image.convert('RGB')
    for x in range(200):
        for y in range(30):
            (r, g, b) = rgb.getpixel((x, y))
            # if (r, g, b) == (204, 213, 204) or (r, g, b) == (255, 213, 255) or (r, g, b) == (204, 170, 204) \
            #         or (r, g, b) == (255, 255, 204) or (r, g, b) == (204, 170, 153) or (r, g, b) == (255, 213, 204) \
            #         or (r, g, b) == (204, 255, 204) or (r, g, b) == (153, 170, 153) or (r, g, b) == (204, 255, 255) \
            #         or (r, g, b) == (204, 213, 255) or (r, g, b) == (153, 213, 153) or (r, g, b) == (204, 213, 255) \
            #         or (r, g, b) == (153, 170, 204) or (r, g, b) == (153, 213, 204) or (r, g, b) == (204, 213, 153) \
            #         or (r, g, b) == (255, 255, 255):
            #     rgb.putpixel((x, y), (255, 255, 255))
            # else:
            #     rgb.putpixel((x, y), (0, 0, 0))
            if r in (51, 102, 153, 204, 255) and g in (43, 85, 128, 170, 213, 255) and b in (51, 102, 153, 204, 255):
                rgb.putpixel((x, y), (255, 255, 255))
    rgb = rgb.convert('L').point(table, '1')
    # rgb.show()
    image.close()
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
        result = "Error occurred in OCR."
    print i, result
print "success"
