import random

import requests

from swiper import config

def gen_vcode(size=4):
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    return random.randint(start, end)

def send_sms(phone):

    params = config.YZX_PARAMS.copy()

    params['mobile'] = phone
    params['param'] = gen_vcode()

    resp = requests.post(config.YZX_URL, json=params)

    if resp.status_code == 200:
        result = resp.json()
        if result['code'] == '000000':
            return True, 'OK'
        else:
            return False, result['msg']
    else:
        return False, '访问短信服务器有误'

