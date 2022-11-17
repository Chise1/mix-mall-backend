# -*- encoding: utf-8 -*-
"""
@File    : utils.py
@Time    : 2022/11/17 17:20
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import uuid

# from fast_tmp.conf import settings
import hashlib


def dict_2_xml(**kwargs) -> str:
    sub = []
    for k, v in kwargs.items():
        sub.append(f"<{k}>{v}</{k}>")
    return f"<xml>{''.join(sub)}</xml>"


def sign(data: dict, secret: str):
    """
    微信小程序加密
    """
    data_tuple = [(k, v) for k, v in data.items()]
    data_tuple.sort(key=lambda k: k[0])
    data_str = "&".join([f"{i[0]}={i[1]}" for i in data_tuple])
    stringSignTemp = data_str + "&key=" + secret  # 注：key为商户平台设置的密钥key
    sign_str = hashlib.md5(stringSignTemp.encode()).hexdigest()
    return sign_str.upper()


if __name__ == '__main__':
    data = {
        "appid": "123",
        "mch_id": "123",
        "nonce_str": str(uuid.uuid4()).replace("-", ""),
        "body": "订单。。。",
        "out_trade_no": "123",
        "total_fee": 100,
        "spbill_create_ip": "127.0.0.1",
        "notify_url": "http://127.0.0.1:8080/ddd",
        "trade_type": "JSAPI",
    }
    sign_str = sign(data, "123")
    data["sign"] = sign_str
    print(dict_2_xml(**data))
