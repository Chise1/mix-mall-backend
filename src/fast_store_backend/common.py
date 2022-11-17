import uuid

import aiohttp

from fast_store_backend.utils import sign


async def place_order(
    appid: str,
    mch_id: str,
    body: str,
    out_trade_no: str,
    total_fee: int,
    spbill_create_ip: str,
    notify_url: str,
    secret: str
):
    """
    :param appid: 微信分配的小程序ID
    :param mch_id: 微信支付分配的商户号
    :param body: 商品简单描述，该字段请按照规范传递。
    :param out_trade_no: 商户系统内部订单号，要求32个字符内，只能是数字、大小写字母_-|*且在同一个商户号下唯一。详见商户订单号
    :param total_fee: 订单总金额，单位为分
    :param spbill_create_ip: 支持IPV4和IPV6两种格式的IP地址。调用微信支付API的机器IP
    :param notify_url: 异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。公网域名必须为https，如果是走专线接入，使用专线NAT IP或者私有回调域名可使用http。
    :param secret: 小程序秘钥
    """
    data = {
        "appid": appid,
        "mch_id": mch_id,
        "nonce_str": str(uuid.uuid4()).replace("-", ""),
        "body": body,
        "out_trade_no": out_trade_no,
        "total_fee": total_fee,
        "spbill_create_ip": spbill_create_ip,
        "notify_url": notify_url,
        "trade_type": "JSAPI",
    }
    sign_str = sign(data, secret)
    data["sign"] = sign_str
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()
