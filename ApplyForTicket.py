# -*- coding: utf-8 -*-
import requests
import re
import urllib
from config import TESTUID, TESTPW, KEYWORD_J
from OCR import ocr
from GrabInformation import grab


def apply(uid, pw, date=10):
    # 为相关参数进行url编码
    keyword = urllib.quote(KEYWORD_J.encode("Shift_JIS"))
    if date == 10:
        eventtarget = "dgd1%24_ctl2%24lkbKouen"
        selkibou1 = "2017061010001"
    else:
        eventtarget = "dgd1%24_ctl3%24lkbKouen"
        selkibou1 = "2017061110001"
    # 创建session
    session = requests.session()
    # 访问活动页
    resp = session.get('http://www.cnplayguide.com/evt/evtlst.aspx?kcd=79654')
    # 获得VIEWSTATE, VIEWSTATESENERATOR和scd
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 0, 1, 0)
    if error == 1:
        print "Failed in line 26."
        return 1
    # 访问6.10详情页
    data = '__EVENTTARGET=' + eventtarget + '&' \
           '__EVENTARGUMENT=&' \
           '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'Keyword=' + keyword + '&' \
           'scd=' + scd + '&' \
           'CnSimulation=&' \
           'dmf='
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '1468',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'www.cnplayguide.com',
        'Origin': 'http://www.cnplayguide.com',
        'Referer': 'http://www.cnplayguide.com/evt/evtlst.aspx?kcd=79654',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36'
    }
    resp = session.post('http://www.cnplayguide.com/evt/evtlst.aspx?kcd=79654', data=data, headers=headers)
    # print resp.history
    # 获取targeturl
    reg_targeturl = ur"MM_openBrWindow\('(.*?)',"
    try:
        targeturl = re.search(reg_targeturl, resp.text).group(1)
    except:
        print "Failed in line 60."
        return 1
    # 打开申请窗口
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'www.cnplayguide.com',
        'Referer': 'http://www.cnplayguide.com/evt/evtdtl.aspx?ecd=CNI21395',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36'
    }
    resp = session.get(targeturl, headers=headers)
    # 获得VIEWSTATE, VIEWSTATESENERATOR, sid和imgaddr
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 1)
    if error == 1:
        print "Failed in line 81."
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
            imageauth = ocr()
        # 发送表单
        data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
               '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
               'selKibou1=' + selkibou1 + '&' \
               'rdbSekishu_1=2X&' \
               'selMaisu_1_2X_1=1&' \
               'hdnZaikoFlg_1_2X_1=0&' \
               'imageauth=' + imageauth + '&' \
               'LOGINUSER=' + uid + '&' \
               'LOGINPASS=' + pw + '&' \
               'next.x=27&' \
               'next.y=5&' \
               'sid=' + sid + '&' \
               'hidMaxMaisu=1&' \
               'shiteiFukusuFlg=1'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Content-Length'] = '4344'
        headers['Origin'] = 'https://www.cnplayguide.com'
        headers['Referer'] = targeturl
        resp = session.post(targeturl, data=data, headers=headers)
        # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
        (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
        if error == 1:
            print "Failed in line 117."
            return 1
        # 检查验证码
        reg5 = ur'入力した文字が画像と一致しません'
        if re.search(reg5, resp.text) is None:
            print "Verify code passed."
            failure = 0
        else:
            # 验证码错误
            print "Verify code failed."
            # 返回
            headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
            resp = session.get(targeturl, headers=headers, cookies=session.cookies)
            # 获得VIEWSTATE, VIEWSTATESENERATOR, sid和imgaddr
            (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 1)
            if error == 1:
                print "Failed in line 133."
                return 1
    # 确认支付方式
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'ksigrdrdo=30%2C0%2C1%2C0%2C0&' \
           'cardtxt1=&' \
           'cardtxt2=&' \
           'cardtxt3=&' \
           'cardtxt4=&' \
           'cardsectxt1=&' \
           'cardsel1=01&' \
           'cardsel2=17&' \
           'cardnamesei=&' \
           'cardnamemei=&' \
           'mailcheck=mailcheck&' \
           'imgbtnnext.x=34&' \
           'imgbtnnext.y=3&' \
           'sid=' + sid + '&' \
           'futaiKbnMiasu=%2C1'
    headers['Content-Length'] = '8269'
    resp = session.post('https://www.cnplayguide.com/rsv/stslc_l.aspx', data=data, headers=headers)
    # 获得VIEWSTATE, VIEWSTATESENERATOR和sid
    (VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error) = grab(resp.text, 1, 1, 1, 0, 0)
    if error == 1:
        print "Failed in line 158."
        return 1
    # 最终确认
    data = '__VIEWSTATE=' + VIEWSTATE_url + '&' \
           '__VIEWSTATEGENERATOR=' + VIEWSTATEGENERATOR + '&' \
           'moushikomi.x=45&' \
           'moushikomi.y=12&' \
           'sid=' + sid + '&' \
           'futaiflg='
    headers['Content-Length'] = '2097'
    headers['Referer'] = 'https://www.cnplayguide.com/rsv/stslc_l.aspx'
    resp = session.post('https://www.cnplayguide.com/rsv/apconf_l.aspx', data=data, headers=headers)
    # 注册成功
    reg5 = ur'お申込が完了いたしました。'
    if re.search(reg5, resp.text) is None:
        return 1
    else:
        return 0

if __name__ == '__main__':
    print "Start testing with uid(%s) and pw(%s)" % (TESTUID, TESTPW)
    if apply(TESTUID, TESTPW, 10):
        print "Failure."
    else:
        print "Success."
    if apply(TESTUID, TESTPW, 11):
        print "Failure."
    else:
        print "Success."
