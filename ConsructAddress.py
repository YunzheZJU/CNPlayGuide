# -*- coding: utf-8 -*-
import math

with open('mailaddress.txt', 'w') as madd:
    for x in range(1, 32):
        b = bin(x).replace('0b', '')
        c = [b for b in b]
        i = int(29 - math.floor(math.log(x, 2))) - 1
        for j in range(i):
            c.insert(0, '0')
        d = "a7856943377856943377856943377"
        e = [d for d in d]
        f = ''
        for i in range(29):
            f = f + e[i] + '.' * int(c[i])
        print f + '8@gmail.com'
        madd.write(f + '8@gmail.com\n')
