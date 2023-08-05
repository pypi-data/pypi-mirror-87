#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import requests
from requests.adapters import HTTPAdapter
import re
import json

import sys
import time
import hashlib

import socket

# from gevent import socket
_dnscache = {}


def _setDNSCache():
    """
    设置DNS缓存
    :return:
    """
    def _getaddrinfo(*args, **kwargs):
        if args in _dnscache:
            return _dnscache[args]
        else:
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo


def get_random_phone():
    """
    获取一个随机手机名称/厂商/型号/版本号
    :return:
    """
    phone_json = {
        "release": [
            "7.0",
            "7.0.1",
            "7.1",
            "8.0",
            "5.1",
            "4.4.4",
            "6.0.1",
            "5.1.1",
            "6.0",
            "4.4.2",
            "5.0.2",
            "4.3",
            "5.0",
            "4.2.2",
            "4.4",
            "4.1.2",
            "5.0.1",
            "4.2.1",
            "4.1.1",
            "4.4.3",
            "4.0.4",
            "4.0.3",
            "4.2",
            "4.1",
            "5.1.0",
            "4.4.5",
            "4.0",
            "4.3.1",
            "4.4.0",
            "5.0.5",
            "5.3",
            "6.0.2",
            "6.1",
            "4.3.0",
            "4.2.3",
            "4.2.9",
            "4.4.1"],
        "phone": [
            {
                "name": "荣耀7i",
                "manufacturer": "HUAWEI",
                "model": "ATH-AL00"
            },
            {
                "name": "荣耀6至尊版",
                "manufacturer": "HUAWEI",
                "model": "H60-L21"
            },
            {
                "name": "荣耀6 Plus",
                "manufacturer": "HUAWEI",
                "model": "PE-TL10"
            },
            {
                "name": "P10",
                "manufacturer": "HUAWEI",
                "model": "VTR-AL00"
            },
            {
                "name": "P10 Plus",
                "manufacturer": "HUAWEI",
                "model": "VKY-AL00"
            },
            {
                "name": "联想K3",
                "manufacturer": "Lenovo",
                "model": "Lenovo K30-T"
            },
            {
                "name": "乐视2",
                "manufacturer": "LeMobile",
                "model": "Le X620"
            },
            {
                "name": "乐视2 Pro",
                "manufacturer": "LeMobile",
                "model": "Le X525"
            },
            {
                "name": "乐视1",
                "manufacturer": "Letv",
                "model": "X600"
            },
            {
                "name": "乐视1 Pro",
                "manufacturer": "Letv",
                "model": "X800+"
            },
            {
                "name": "乐视1 S",
                "manufacturer": "Letv",
                "model": "Letv X500"
            },
            {
                "name": "乐视1 S 太子妃版",
                "manufacturer": "Letv",
                "model": "Letv X501"
            },
            {
                "name": "HTC One M9",
                "manufacturer": "HTC",
                "model": "HTC M9e"
            },
            {
                "name": "HTC One A9",
                "manufacturer": "HTC",
                "model": "HTC One A9"
            },
            {
                "name": "HTC One M9",
                "manufacturer": "HTC",
                "model": "HTC M9e"
            },
            {
                "name": "HTC One A9",
                "manufacturer": "HTC",
                "model": "HTC One A9"
            },
            {
                "name": "OPPO R9",
                "manufacturer": "OPPO",
                "model": "OPPO R9m"
            },
            {
                "name": "OPPO Find7",
                "manufacturer": "OPPO",
                "model": "x9007"
            },
            {
                "name": "OPPO Find5",
                "manufacturer": "OPPO",
                "model": "x909t"
            },
            {
                "name": "OPPO R7",
                "manufacturer": "OPPO",
                "model": "OPPO R7"
            },
            {
                "name": "OPPO R7S",
                "manufacturer": "OPPO",
                "model": "OPPO R7S"
            },
            {
                "name": "锤子 T1",
                "manufacturer": "Smartisan",
                "model": "SM705"
            },
            {
                "name": "锤子 T2",
                "manufacturer": "Smartisan",
                "model": "SM801"
            },
            {
                "name": "坚果",
                "manufacturer": "Smartisan",
                "model": "YQ601"
            },
            {
                "name": "锤子 T3",
                "manufacturer": "Smartisan",
                "model": "SM901"
            },
            {
                "name": "小米2S",
                "manufacturer": "Xiaomi",
                "model": "MI 2S"
            },
            {
                "name": "小米3",
                "manufacturer": "Xiaomi",
                "model": "MI 3"
            },
            {
                "name": "小米4",
                "manufacturer": "Xiaomi",
                "model": "MI 4LTE"
            },
            {
                "name": "小米4C",
                "manufacturer": "Xiaomi",
                "model": "MI-4C"
            },
            {
                "name": "小米4S",
                "manufacturer": "Xiaomi",
                "model": "MI 4S"
            },
            {
                "name": "小米5",
                "manufacturer": "Xiaomi",
                "model": "MI 5"
            },
            {
                "name": "小米NOTE",
                "manufacturer": "Xiaomi",
                "model": "MI NOTE LTE"
            },
            {
                "name": "小米MAX",
                "manufacturer": "Xiaomi",
                "model": "MI MAX"
            },
            {
                "name": "小米NOTE 2",
                "manufacturer": "Xiaomi",
                "model": "MI NOTE 2"
            },
            {
                "name": "小米NOTE 顶配版",
                "manufacturer": "Xiaomi",
                "model": "MI NOTE PRO"
            },
            {
                "name": "红米Note3",
                "manufacturer": "Xiaomi",
                "model": "Redmi Note 3"
            },
            {
                "name": "小米平板2",
                "manufacturer": "Xiaomi",
                "model": "MI Pad 2"
            },
            {
                "name": "小米5S",
                "manufacturer": "Xiaomi",
                "model": "2016080 "
            },
            {
                "name": "小米 Note 4",
                "manufacturer": "Xiaomi",
                "model": "2016060"
            },
            {
                "name": "小米MIX",
                "manufacturer": "Xiaomi",
                "model": "MIX"
            },
            {
                "name": "一加手机1",
                "manufacturer": "OnePlus",
                "model": "A1001"
            },
            {
                "name": "一加手机2",
                "manufacturer": "OnePlus",
                "model": "ONE A2001"
            },
            {
                "name": "一加手机3",
                "manufacturer": "OnePlus",
                "model": "OnePlus A3000"
            },
            {
                "name": "中兴 AXON 天机 MAX",
                "manufacturer": "ZTE",
                "model": "ZTE C2016"
            },
            {
                "name": "中兴 AXON 天机 MINI",
                "manufacturer": "ZTE",
                "model": "ZTE B2015"
            },
            {
                "name": "中兴 AXON 天机",
                "manufacturer": "ZTE",
                "model": "ZTE A2015"
            },
            {
                "name": "中兴 星星2号",
                "manufacturer": "ZTE",
                "model": "ZTE G720C"
            },
            {
                "name": "努比亚Z11 mini全网通",
                "manufacturer": "ZTE",
                "model": "NX529J"
            },
            {
                "name": "努比亚大牛 Z9 Max",
                "manufacturer": "ZTE",
                "model": "NX512J"
            },
            {
                "name": "努比亚小牛4 Z9 Mini",
                "manufacturer": "ZTE",
                "model": "NX511J"
            },
            {
                "name": "ZTE国民指纹机BladeA1",
                "manufacturer": "ZTE",
                "model": "ZTE C880U"
            },
            {
                "name": "格力手机1",
                "manufacturer": "GREE",
                "model": "G0111"
            },
            {
                "name": "格力手机1s",
                "manufacturer": "GREE",
                "model": "G0121"
            },
            {
                "name": "格力手机2",
                "manufacturer": "GREE",
                "model": "G0128"
            },
            {
                "name": "MX2",
                "manufacturer": "Meizu",
                "model": "MX2"
            },
            {
                "name": "MX3",
                "manufacturer": "Meizu",
                "model": "M355"
            },
            {
                "name": "MX4",
                "manufacturer": "Meizu",
                "model": "MX4"
            },
            {
                "name": "MX4 Pro",
                "manufacturer": "Meizu",
                "model": "MX4 Pro"
            },
            {
                "name": "MX5",
                "manufacturer": "Meizu",
                "model": "M575M"
            },
            {
                "name": "PRO 6",
                "manufacturer": "Meizu",
                "model": "PRO 6"
            },
            {
                "name": "魅蓝3",
                "manufacturer": "Meizu",
                "model": "魅蓝3"
            },
            {
                "name": "魅蓝 note",
                "manufacturer": "Meizu",
                "model": "m1 note"
            },
            {
                "name": "魅蓝3 note",
                "manufacturer": "Meizu",
                "model": "m3 note"
            },
            {
                "name": "魅蓝metal",
                "manufacturer": "Meizu",
                "model": "m1 metal"
            },
            {
                "name": "Galaxy S6 Edge+",
                "manufacturer": "samsung",
                "model": "SM-G9280"
            },
            {
                "name": "Galaxy Note7",
                "manufacturer": "samsung",
                "model": "SM-N9300"
            },
            {
                "name": "Galaxy S7 edge",
                "manufacturer": "samsung",
                "model": "SM-G9350"
            },
            {
                "name": "Galaxy S7",
                "manufacturer": "samsung",
                "model": "SM-G9300"
            },
            {
                "name": "Galaxy S8",
                "manufacturer": "samsung",
                "model": "SM-G9500"
            },
            {
                "name": "Galaxy S8+",
                "manufacturer": "samsung",
                "model": "SM-G9550"
            },
            {
                "name": "Galaxy C7",
                "manufacturer": "samsung",
                "model": "SM-W2017 "
            },
            {
                "name": "Galaxy ON5",
                "manufacturer": "samsung",
                "model": "SM-G5520"
            },
            {
                "name": "Galaxy ON5",
                "manufacturer": "samsung",
                "model": "SM-G5520"
            },
            {
                "name": "Galaxy C9 Pro",
                "manufacturer": "samsung",
                "model": "SM-C9000"
            },
            {
                "name": "Xperia Z3",
                "manufacturer": "Sony",
                "model": "L55t"
            },
            {
                "name": "Xperia Z5 Premium",
                "manufacturer": "Sony",
                "model": "E6883"
            },
            {
                "name": "Xperia Z5",
                "manufacturer": "Sony",
                "model": "E6683"
            },
            {
                "name": "Xperia Z3+",
                "manufacturer": "Sony",
                "model": "E6533"
            }
        ]
    }
    array_phone = phone_json['phone']
    pid = random.randint(1, len(array_phone) - 1)
    item_phone = array_phone[pid]
    name = item_phone['name'].replace(' ', '')
    manufacturer = item_phone['manufacturer'].replace(' ', '')
    model = item_phone['model'].replace(' ', '')
    array_release = phone_json['release']
    rid = random.randint(1, len(array_release) - 1)
    release = array_release[rid]
    print(name, manufacturer, model, release)
    return name, manufacturer, model, release


def randomIP():
    a = random.sample(list(range(1, 256)) * 4, 4)
    b = map(str, a)
    ip = '.'.join(b)
    return ip


def get_fake_headers():
    fakeHeaders = {"X-Forwarded-For": randomIP() + ',' + randomIP() + ',' + randomIP(), "X-Forwarded": randomIP(),
                   "Forwarded-For": randomIP(), "Forwarded": randomIP(),
                   "X-Forwarded-Host": randomIP(), "X-remote-IP": randomIP(),
                   "X-remote-addr": randomIP(), "True-Client-IP": randomIP(),
                   "X-Client-IP": randomIP(), "Client-IP": randomIP(), "X-Real-IP": randomIP(),
                   "Ali-CDN-Real-IP": randomIP(), "Cdn-Src-Ip": randomIP(), "Cdn-Real-Ip": randomIP(),
                   "X-Cluster-Client-IP": randomIP(),
                   "WL-Proxy-Client-IP": randomIP(), "Proxy-Client-IP": randomIP(),
                   "Fastly-Client-Ip": randomIP(), "True-Client-Ip": randomIP()
                   }
    return fakeHeaders


def get_random_string(num=32):
    ran_str = ''.join(random.sample('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678', num))
    return ran_str


def get_random_mobile():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


def get_random_nick_and_avatar():
    nickName = ''
    avatar = ''
    try:
        while nickName == '':
            QQ = random.randint(888888, 99999999)
            avatar = 'http://q1.qlogo.cn/g?b=qq&nk={QQ}&s=100'.format(QQ=QQ)
            url = 'https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={QQ}'.format(QQ=QQ)
            try:
                resp = requests.get(url, timeout=3)
                nickName = re.findall('0,0,0,"(.*?)"', resp.content.decode('gbk'))[0]
            except Exception as e:
                pass
        return nickName, avatar
    except Exception as e:
        print(e)
        return '', ''


class RabbitHttp:
    def __init__(self, timeout=5, post_headers={}, get_headers={}, fake_ip=True, ):
        """
        :param timeout: : 每个请求的超时时间
        :param post_headers: POST协议头
        :param get_headers: GET协议头
        :param fake_ip: 是否开启随机ip
        """
        self.get_headers = get_headers
        self.post_headers = post_headers
        s = requests.Session()
        #: 在session实例上挂载Adapter实例, 目的: 请求异常时,自动重试
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        #: 设置为False, 主要是HTTPS时会报错, 为了安全也可以设置为True
        s.verify = True

        #: 公共的请求头设置
        fakeHeaders = {"X-Forwarded-For": randomIP() + ',' + randomIP() + ',' + randomIP(), "X-Forwarded": randomIP(),
                       "Forwarded-For": randomIP(), "Forwarded": randomIP(),
                       "X-Forwarded-Host": randomIP(), "X-remote-IP": randomIP(),
                       "X-remote-addr": randomIP(), "True-Client-IP": randomIP(),
                       "X-Client-IP": randomIP(), "Client-IP": randomIP(), "X-Real-IP": randomIP(),
                       "Ali-CDN-Real-IP": randomIP(), "Cdn-Src-Ip": randomIP(), "Cdn-Real-Ip": randomIP(),
                       "X-Cluster-Client-IP": randomIP(),
                       "WL-Proxy-Client-IP": randomIP(), "Proxy-Client-IP": randomIP(),
                       "Fastly-Client-Ip": randomIP(), "True-Client-Ip": randomIP()
                       }
        if fake_ip:
            post_headers.update(fakeHeaders)
            get_headers.update(fakeHeaders)

        #: 挂载到self上面
        self.s = s
        self.s.timeout = timeout

    def get(self, url):
        """GET

        :param url:
        :param query_dict: 一般GET的参数都是放在URL查询参数里面
        :return:
        """
        print('GET==>' + url)
        return self.s.get(url, headers=self.get_headers)

    def post(self, url, form_data=None, body_dict=None):
        """POST

        :param url:
        :param form_data: 有时候POST的参数是放在表单参数中
        :param body_dict: 有时候POST的参数是放在请求体中(这时候 Content-Type: application/json )
        :return:
        """
        if form_data:
            print('POST==>' + url)
            print('DATA==>', str(form_data))
            return self.s.post(url, data=form_data, headers=self.post_headers)
        if body_dict:
            print('POST==>' + url)
            print('JSON==>', str(body_dict))
            return self.s.post(url, json=body_dict, headers=self.post_headers)

    def __del__(self):
        """当实例被销毁时,释放掉session所持有的连接

        :return:
        """
        if self.s:
            self.s.close()


if __name__ == '__main__':
    get_random_phone()
