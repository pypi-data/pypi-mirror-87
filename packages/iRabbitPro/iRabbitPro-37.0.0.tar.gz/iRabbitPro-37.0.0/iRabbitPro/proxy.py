#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
from iRabbitPro.irabbit import RabbitHttp


def get_proxy(num):
    i = RabbitHttp()
    url = f'http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=60&cid=-1&orderId=O20100301555849667354&time=1606747841&sign=eb7b8d7663a2932ca10330f6736d4ab9&noDuplicate=1&dataType=1&lineSeparator=0&singleIp=0'
    try:
        resp = i.get(url)
        if ':' in resp.text:
            print(f'获取到{num}个代理IP:' + resp.text)
            return resp.text
        else:
            time.sleep(3)
            print(f'重新获取代理IP..' + resp.text)
            get_proxy(num)
    except Exception as e:
        print(e)
        time.sleep(3)
        get_proxy(num)
