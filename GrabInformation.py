# -*- coding: utf-8 -*-
import re


def grab(text, flag_v, flag_vg, flag_sid, flag_scd, flag_i):
    reg_viewstate = ur'id="__VIEWSTATE" value="(.*?)"'
    reg_viewstategenerator = ur'id="__VIEWSTATEGENERATOR" value="(.*?)"'
    reg_sid = ur'id="sid" value="(.*?)"'
    reg_scd = ur'id="scd" value="(.*?)"'
    reg_nm = ur'nm=(.*?)"'
    VIEWSTATE_url = "Fail to get VIEWSTATE"
    VIEWSTATEGENERATOR = "Fail to get VIEWSTATEGENERETOR"
    sid = "Fail to get sid"
    scd = "Fail to get scd"
    imgaddr = "Fail to get img address"
    error = 0
    try:
        if flag_v:
            VIEWSTATE = re.search(reg_viewstate, text).group(1)
            VIEWSTATE_url = VIEWSTATE.replace("/", "%2F").replace("+", "%2B").replace("=", "%3D")
        if flag_vg:
            VIEWSTATEGENERATOR = re.search(reg_viewstategenerator, text).group(1)
        if flag_sid:
            sid = re.search(reg_sid, text).group(1)
        if flag_scd:
            scd = re.search(reg_scd, text).group(1)
        if flag_i:
            imgaddr = "https://www.cnplayguide.com/com/authimg.aspx?nm=" + re.search(reg_nm, text).group(1)
    except:
        print VIEWSTATE_url
        print VIEWSTATEGENERATOR
        print sid
        print scd
        print imgaddr
        error = 1
    return VIEWSTATE_url, VIEWSTATEGENERATOR, sid, scd, imgaddr, error
