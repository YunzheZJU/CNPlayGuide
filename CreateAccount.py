# -*- coding: utf-8 -*-
import requests
import re
import urllib
from config import TESTMAILADDR, KEYWORD_J, MSG_J, SEI_KANJI_J, MEI_KANJI_J, SEI_KANA_J, MEI_KANA_J
from OCR import ocr
from GrabInformation import grab


def create(mailaddr):
    # 为相关参数进行url编码
    mailaddr = urllib.quote(mailaddr)
    keyword = urllib.quote(KEYWORD_J.encode("Shift_JIS"))
    msg = urllib.quote(MSG_J.encode("Shift_JIS"))
    msg_utf8 = MSG_J.encode('unicode_escape').replace('\\', "%")
    sei_kanji = urllib.quote(SEI_KANJI_J.encode("Shift_JIS"))
    mei_kanji = urllib.quote(MEI_KANJI_J.encode("Shift_JIS"))
    sei_kana = urllib.quote(SEI_KANA_J.encode("Shift_JIS"))
    mei_kana = urllib.quote(MEI_KANA_J.encode("Shift_JIS"))
    # 创建session
    session = requests.session()
    # 1. 访问首页
    resp = session.get('http://www.cnplayguide.com')
    # 2. 访问会员申请页面
    resp = session.get('http://www.cnplayguide.com/mem/cpmemcgi.aspx')
    # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
    if error == 1:
        return 1
    # 3. 提交会员申请
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'Keyword=' + keyword + '&' \
           'txtFindKeitaiMail=&' \
           'CN%83v%83%8C%89%EF%88%F5%82%C9%90%5C%82%B5%8D%9E%82%DE.x=55&' \
           'CN%83v%83%8C%89%EF%88%F5%82%C9%90%5C%82%B5%8D%9E%82%DE.y=5&' \
           'sid=' + sid
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '680',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'www.cnplayguide.com',
        'Origin': 'http://www.cnplayguide.com',
        'Referer': 'http://www.cnplayguide.com/mem/cpmemcgi.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36'
    }
    resp = session.post('http://www.cnplayguide.com/mem/cpmemcgi.aspx',
                        data=data, headers=headers, cookies=session.cookies)
    # print resp.history
    # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
    if error == 1:
        return 1
    # 4. 同意条款
    headers['Referer'] = 'http://www.cnplayguide.com/mem/cpmemag.aspx?kkb=03&msg='
    headers['Content-Length'] = '483'
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'Keyword=' + keyword + '&' \
           '%93%AF%88%D3%82%B7%82%E9.x=35&' \
           '%93%AF%88%D3%82%B7%82%E9.y=11&' \
           'sid=' + sid + '&' \
           'kkb=03'
    resp = session.post('http://www.cnplayguide.com/mem/cpmemag.aspx?kkb=03&msg=',
                        data=data, headers=headers, cookies=session.cookies)
    # print resp.history
    # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
    if error == 1:
        return 1
    # 5. 提交表单
    headers['Referer'] = 'https://www.cnplayguide.com/mem/memr_b.aspx?kkb=03&msg='
    headers['Content-Length'] = '2017'
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'Keyword=' + keyword + '&' \
           'txtNAME_SEI_KANJI=' + sei_kanji + '&' \
           'txtNAME_MEI_KANJI=' + mei_kanji + '&' \
           'txtNAME_SEI_KANA=' + sei_kana + '&' \
           'txtNAME_MEI_KANA=' + mei_kana + '&' \
           'txtNICK_NAME=TuTou&' \
           'txtNen=1990&' \
           'drpTuki=01&' \
           'drpHi=01&' \
           'rdosex=1&' \
           'drpSyokuGyo=1&' \
           'txtTEL_JITAKU_1=&' \
           'txtTEL_JITAKU_2=&' \
           'txtTEL_JITAKU_3=&' \
           'txtTEL_KEITAI_1=080&' \
           'txtTEL_KEITAI_2=6600&' \
           'txtTEL_KEITAI_3=0817&' \
           'rdoAddress=1&' \
           'txtPC_ADDRESS=' + mailaddr + '&' \
           'txtKEITAI_ADDRESS=&' \
           'txtPOST_JITAKU1=192&' \
           'txtPOST_JITAKU2=0916&' \
           'drpJitakuKen=13&' \
           'txtJITAKU_SIKUGUN=%94%AA%89%A4%8Eq&' \
           'txtJITAKU_THOUMEI=%82%DD%82%C8%82%DD%96%EC&' \
           'txtJITAKU_BUIL=5-12-7%81%40101&' \
           'rdoDM=2&' \
           '%8E%9F%82%D6.x=35&' \
           '%8E%9F%82%D6.y=11&' \
           'sid=' + sid + '&' \
           'kkb=03'
    resp = session.post('https://www.cnplayguide.com/mem/memr_b.aspx?kkb=03&msg=',
                        data=data, headers=headers, cookies=session.cookies)
    # # print resp.history
    # 获得VIEWSTATE, VIEWSTATESENERATOR, sid和imgaddr
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 1)
    if error == 1:
        return 1
    failure = 1
    while failure:
        # 画像认证
        imageauth = "Error"
        while imageauth == "Error":
            r = requests.get(imgaddr, stream=True)
            with open("img.gif", 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
                    f.flush()
            # Image.open('img.gif').show()
            # imageauth = raw_input("直接输入验证码数字：")
            imageauth = ocr()
        # 6. 提交
        headers['Referer'] = 'https://www.cnplayguide.com/mem/memr_m.aspx?sid=%s&kkb=03&msg=&cnt=58' % sid
        headers['Content-Length'] = '2017'
        data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
               '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
               'Keyword=' + keyword + '&' \
               'rdoArea=00&' \
               'rdoMarumaga=2&' \
               'rdoMyPage=0&' \
               'imageauth=' + imageauth + '&' \
               '%8E%9F%82%D6.x=27&' \
               '%8E%9F%82%D6.y=4&' \
               'hdnKeyword=&' \
               'sid=' + sid + '&' \
               'kkb=03&' \
               'count=58&' \
               'Hidden2=&' \
               'Hidden1=0&' \
               'hdnKeyWordFlg=&' \
               'hdnNextFlg=1&' \
               'hdnGazouHenkoFlg='
        resp = session.post('https://www.cnplayguide.com/mem/memr_m.aspx?sid=%s&kkb=03&msg=&cnt=58' % sid,
                            data=data, headers=headers, cookies=session.cookies)
        # print resp.history
        # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
        (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
        if error == 1:
            return 1
        # 检查验证码
        reg = ur'入力した文字が画像と一致しません'
        if re.search(reg, resp.text) is None:
            print "Verify code passed."
            failure = 0
        else:
            # 验证码错误
            print "Verify code failed."
            # 返回
            headers['Referer'] = 'https://www.cnplayguide.com/mem/memr_m.aspx?sid=%s&kkb=03&msg=%s&cnt=58&kcnt=0' \
                                 % (sid, msg)
            headers['Content-Length'] = '926'
            data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
                   '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
                   'Keyword=' + keyword + '&' \
                   'Imagebutton1.x=38&' \
                   'Imagebutton1.y=12&' \
                   'hdnKeyword=&' \
                   'sid=' + sid + '&' \
                   'kkb=03&' \
                   'count=58&' \
                   'Hidden2=&' \
                   'Hidden1=0&' \
                   'hdnKeyWordFlg=&' \
                   'hdnNextFlg=&' \
                   'hdnGazouHenkoFlg='
            resp = session.post('https://www.cnplayguide.com/mem/memr_m.aspx?sid=%s&kkb=03&msg=%s&cnt=58&kcnt=0'
                                % (sid, msg_utf8), data=data, headers=headers, cookies=session.cookies)
            # 获得VIEWSTATE, VIEWSTATESENERATOR, sid和imgaddr
            (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 1)
            if error == 1:
                return 1
    # 7. 确认内容
    headers['Referer'] = 'https://www.cnplayguide.com/mem/memrconf.aspx?sid=%s&kkb=03&msg=&cnt=58&kcnt=0&mps=0' % sid
    headers['Content-Length'] = '1322'
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'Keyword=' + keyword + '&' \
           '%93o%98%5E.x=32&' \
           '%93o%98%5E.y=9&' \
           'sid=' + sid + '&' \
           'kkb=03'
    resp = session.post('https://www.cnplayguide.com/mem/memrconf.aspx?sid=%s&kkb=03&msg=&cnt=58&kcnt=0&mps=0' % sid,
                        data=data, headers=headers, cookies=session.cookies)
    # # print resp.history
    # 注册成功
    reg = ur'CNプレ会員への登録が完了しました。'
    if re.search(reg, resp.text) is None:
        reg = ur'ご入力された会員情報は既に登録されています。'
        if re.search(reg, resp.text) is None:
            return 1
        else:
            with open('mailaddressfinished.txt', 'a') as maddrf:
                maddrf.write("%s has been Used.\n" % mailaddr)
    else:
        return 0

if __name__ == '__main__':
    print "Start testing with E-mail: " + TESTMAILADDR
    if create(TESTMAILADDR):
        print "We met with some error. Creating may fail. Please check confirmation e-mail first."
    else:
        print "Succeeded."
