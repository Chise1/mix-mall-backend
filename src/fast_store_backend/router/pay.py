from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter(prefix="/pay")


# todo 需要增加查询接口 3、在订单状态不明或者没有收到微信支付结果通知的情况下，建议商户主动调用微信支付【查询订单API】确认订单状态。
@router.post("/notify_info")
async def notify_info(request: Request):
    """
    支付回调通知信息
    """
    print(await request.json())  # todo需要对接之后再测试
    return """
    <xml>
  <return_code>SUCCESS</return_code>
  <return_msg>OK</return_msg>
</xml>
"""
