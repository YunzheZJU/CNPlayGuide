# -*- coding: utf-8 -*-
import time
from CreateAccount import create
from ApplyForTicket import apply
from GetMail import get


with open('mailaddress.txt', 'r') as maddr:
    errortime = 0
    for line in maddr.readlines():
        address = line.strip()
        print address
        with open('mailaddressfinished.txt', 'a') as maddrf:
            localtime = time.asctime(time.localtime(time.time()))
            maddrf.write(localtime + ' ' + line)
        if create(address):
            errortime += 1
            print "We met with some error. Creating may fail. Please check confirmation e-mail first. %s" % address
            with open('mailaddressfinished.txt', 'a') as maddrf:
                maddrf.write("We met with some error. Creating may fail. Please check confirmation e-mail first. %s\n" % address)
            continue
        else:
            print "Succeeded in creating account."
        uid, pw = get()
        if uid:
            print "Succeeded in getting uid and pw."
            for d in range(10, 12):
                if apply(str(uid), str(pw), d):
                    errortime += 1
                    print "Apply for Day %s's ticket failed. %s" % (d, address)
                    with open('mailaddressfinished.txt', 'a') as maddrf:
                        maddrf.write("Apply for Day %s's ticket failed. %s\n" % (d, address))
                else:
                    print "Apply for Day %s's ticket succeed." % d
        else:
            errortime += 1
            print "Get UID failed. Please check email by yourself. %s" % address
            with open('mailaddressfinished.txt', 'a') as maddrf:
                maddrf.write("Get UID failed. Please check email by yourself. %s\n" % address)
        if errortime >= 10:
            exit(1)
