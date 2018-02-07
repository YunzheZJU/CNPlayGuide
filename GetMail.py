# -*- coding: utf-8 -*-
import imaplib
import email
import time
import re
from config import MAIL_UN, MAIL_PW


def get():
    num = -1
    # 创建连接
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    # 登录
    conn.login(MAIL_UN, MAIL_PW)
    # 获得邮件列表
    for i in range(10):
        conn.select("INBOX")
        type1, data = conn.search(None, 'UNSEEN')
        # 获得最近邮件
        msgList = data[0].split()
        try:
            type2, data = conn.fetch(msgList[num], '(RFC822)')
        except:
            print "No new email! Wait for 5 seconds..."
            time.sleep(5)
            continue
        msg = email.message_from_string(data[0][1])
        try:
            content = msg.get_payload().decode('iso-2022-jp')
        except:
            print "The newest email is not encoded with iso-2022-jp!"
            continue
        reg_uid = ur'ユーザーＩＤ：(.*?)\n'
        reg_pw = ur'パスワード：(.*?)\n'
        try:
            uid = re.search(reg_uid, content).group(1).split()[0]
            pw = re.search(reg_pw, content).group(1).split()[0]
            conn.close()
            conn.logout()
            return uid, pw
        except:
            print "No uid found or error occurred."
    conn.close()
    conn.logout()
    return 0, 0

if __name__ == '__main__':
    get()
