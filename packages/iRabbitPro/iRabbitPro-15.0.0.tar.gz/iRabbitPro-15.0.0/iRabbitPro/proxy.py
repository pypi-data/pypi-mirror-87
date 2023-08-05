import time
import requests


def get_proxy(num):
    url = f'http://api.hailiangip.com:8422/api/getIp?type=1&num={num}&pid=-1&unbindTime=60&cid=-1&orderId=O20100301555849667354&time={int(time.time())}&sign=327524bf470ff93d6ec893f759472aa3&noDuplicate=1&dataType=1&lineSeparator=0&singleIp=0'
    resp = requests.get(url)
    print(f'获取到{num}个代理IP:' + resp.text)
    return resp.text
