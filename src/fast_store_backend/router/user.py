import json
import time
import uuid
from typing import Optional, List
import aiohttp
from fast_tmp.conf import settings
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from tortoise.expressions import F
from tortoise.query_utils import Prefetch

from fast_store_backend.common import place_order
from fast_store_backend.dantic_model import CreateOrderInfo
from fast_store_backend.depends import get_customer, get_customer_or_none, create_token
from fast_store_backend.models import Customer, Goods, Address, GoodsHistory, GoodsSku, Order, \
    OrderSub, OrderState, Cart
from tortoise.transactions import in_transaction

from fast_store_backend.responses import ErrInfo
from fast_store_backend.utils import sign

router = APIRouter(prefix="/user")


@router.get("/addresses")
async def get_address(customer: Customer = Depends(get_customer)):
    return await Address.filter(customer=customer)


@router.get("/address/default")
async def get_default_address(customer: Customer = Depends(get_customer)):
    return await Address.filter(customer=customer, isDefault=True).first()


class CreateAddress(BaseModel):
    id: Optional[int] = None
    name: str
    mobile: str
    province: str
    city: str
    district: str
    address: str
    isDefault: bool = False


@router.post("/address")
async def create_address(info: CreateAddress, customer: Customer = Depends(get_customer)):
    data = info.dict(exclude_none=True)

    async  with in_transaction() as conn:
        if info.isDefault:
            await Address.filter(customer=customer).using_db(conn).update(isDefault=False)
        if info.id:
            data.pop("id")
            await Address.filter(pk=info.id).using_db(conn).update(**data)
        else:
            await Address.create(**data, customer=customer)


@router.get("/userInfo")
async def userinfo(customer: Customer = Depends(get_customer)):
    """
    读取客户信息
    """
    return {
        "nickName": customer.nickName,
        "gender": customer.gender,
        "avatarUrl": customer.avatarUrl,
    }


@router.get("/view_history")
async def get_user_view_history(customer: Customer = Depends(get_customer_or_none)):
    """
    获取客户浏览历史记录
    """
    if not customer:
        return []
    return await Goods.filter(history__customer=customer).order_by("-history__add_time").limit(
        10).values("id", "name", "image", "history__add_time")


@router.get("/loginByWeixin")
async def wechat_login(request: Request, code: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.EXTRA_SETTINGS['WECHAT_APPID']}&secret={settings.EXTRA_SETTINGS['WECHAT_SECRET']}&js_code={code}&grant_type=authorization_code")
        data = json.loads(await response.text())
        openid = data.get("openid")
        if not openid:
            return JSONResponse(content={"msg": data["errmsg"], "status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer = await Customer.filter(openid=openid).first()
        if customer and customer.nickName:
            return {"token": create_token(customer), "registered": True}
        if not customer:
            customer = Customer(**data)
            await customer.save()
            return {"token": create_token(customer), "registered": False}
        return {"token": create_token(customer), "registered": False}


@router.post("/userInfo")
async def update_userInfo(request: Request, customer: Customer = Depends(get_customer)):
    data = await request.json()  # {'nickName': '微信用户', 'gender': 0, 'language': '', 'city': '', 'province': '', 'country': '', 'avatarUrl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/POgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg/132'}
    customer.nickName = data["nickName"]
    await Customer.filter(pk=customer.pk).update(**data)


@router.post("/favorite")
async def favorite(goods_id: int, favorite: bool, customer: Customer = Depends(get_customer)):
    """
    收藏或取消收藏
    """
    await GoodsHistory.filter(goods_id=goods_id, customer=customer).update(favorite=favorite)
    return {"favorite": favorite}


@router.post("/order")
async def create_order(orderinfo: CreateOrderInfo, customer: Customer = Depends(get_customer)):
    """
    创建订单
    """
    sku_list = []
    goods_list = []
    err_info = ""
    price = 0
    ordersub = []
    cartList = []
    for i in orderinfo.goodsList:
        if i.cart_id:
            cartList.append(i.cart_id)
        if not i.sku_id:
            goods = await Goods.filter(pk=i.goods_id).first()
            if not goods or goods.spec_type:
                raise ErrInfo(status_code=400, detail="数据错误")
            if goods.stock_num < i.num:
                err_info += f"{goods.name}库存不足"
            else:
                goods_list.append(goods)
                price += goods.price * i.num
                ordersub.append(
                    OrderSub(
                        goods=goods, price=goods.price, number=i.num, attrs="-",
                        stock_num=goods.stock_num, preview=goods.image, name=goods.name
                    )
                )
        else:
            sku = await GoodsSku.filter(pk=i.sku_id).prefetch_related("goods").first()
            if not sku:
                raise ErrInfo(status_code=400, detail="数据错误")
            if sku.stock_num < i.num:
                err_info += f"{sku.goods.name}库存不足"
            else:
                sku_list.append(sku)
                price += sku.price * i.num
                ordersub.append(
                    OrderSub(
                        goods=sku.goods, sku=sku, price=sku.price, number=i.num,
                        attrs=sku.attrs, stock_num=sku.stock_num,
                        preview=sku.preview, name=sku.goods.name
                    )
                )
    if err_info != "":
        raise ErrInfo(status_code=400, detail=err_info)
    order = Order(
        price=price,
        remark=orderinfo.remark,
        customer=customer,
        address=orderinfo.address
    )
    async with in_transaction() as conn:
        if len(cartList) > 0:
            await Cart.filter(pk__in=cartList, customer=customer).using_db(conn).delete()
        for i in ordersub:
            stock_num = i.stock_num
            while True:  # 乐观锁
                if not i.sku:
                    ret = await Goods.filter(pk=i.goods.pk, stock_num=stock_num).using_db(
                        conn).update(
                        stock_num=stock_num - i.number)
                    if ret >= 0:
                        i.stock_num = stock_num
                        break
                    else:
                        goods = await Goods.filter(pk=i.goods.pk).using_db(conn).first()
                        stock_num = goods.stock_num
                        if stock_num < i.number:
                            raise ErrInfo(status_code=400, detail=f"{i.name}库存不足")

                else:
                    ret = await GoodsSku.filter(pk=i.sku.pk, stock_num=stock_num).using_db(
                        conn).update(
                        stock_num=stock_num - i.number)
                    if ret >= 0:
                        await Goods.filter(pk=i.goods.pk).using_db(conn).update(
                            stock_num=F("stock_num") - i.number
                        )
                        i.stock_num = stock_num
                        break
                    else:
                        sku = await GoodsSku.filter(pk=i.sku.pk).using_db(conn).first()
                        stock_num = sku.stock_num
                        if stock_num < i.number:
                            raise ErrInfo(status_code=400, detail=f"{i.name}库存不足")
        await order.save(conn)
        for i in ordersub:
            i.order = order
        await OrderSub.bulk_create(ordersub, using_db=conn)
    return {
        "order_id": order.pk,
        "price": price,
    }


@router.get("/orders")
async def get_order(state: Optional[int] = None, next: Optional[int] = None,
                    customer: Customer = Depends(get_customer)):
    """
    获取订单
    """
    queryset = Order.filter(customer=customer)
    if state:
        queryset = queryset.filter(state=state)
    if next:
        queryset = queryset.filter(id__gt=next)
    return [
        {
            "add_time": i.add_time,
            "id": i.pk,
            "logistics_type": i.logistics_type,
            "price": i.price,
            "remark": i.remark,
            "state": i.state,
            "number": sum([goods.number for goods in i.goodsList]),
            "goodsList": [
                {
                    "id": goods.pk,
                    "preview": goods.preview,
                    "name": goods.name,
                    "attrs": goods.attrs,
                    "number": goods.number,
                    "price": goods.price,
                }
                for goods in i.goodsList
            ]
        }
        for i in await queryset.prefetch_related("goodsList")
    ]


@router.delete("/order")
async def del_order(order_id: int, customer: Customer = Depends(get_customer)):
    """
    删除订单
    """
    await Order.filter(pk=order_id, customer=customer).update(state=OrderState.cancel)


@router.post("/pay")
async def order_pay(request: Request, order_id: int, customer: Customer = Depends(get_customer)):
    """
    支付接口
    """
    ip = request.headers.get("host").split(":")[0]
    order = await Order.filter(pk=order_id, customer=customer).prefetch_related(
        "goodsList").first()
    if not order:
        raise ErrInfo(status_code=400, detail="找不到订单")
    pre_pay_res = await place_order(  # todo 增加错误处理
        settings.EXTRA_SETTINGS["WECHAT_APPID"],
        settings.EXTRA_SETTINGS["WECHAT_MCHID"],
        ",".join([i.name for i in order.goodsList]),
        order.trade_no,
        order.price * 100,
        ip,
        settings.EXTRA_SETTINGS["WECHAT_PAY_NOTIFY_URL"],
        settings.EXTRA_SETTINGS["WECHAT_SECRET"],
    )
    pre_pay = pre_pay_res["prepay_id"]
    ret = {
        "appId": settings.EXTRA_SETTINGS["WECHAT_APPID"],
        "timeStamp": str(int(time.time())),
        "nonceStr": str(uuid.uuid4()).replace("-", ""),
        "signType": "MD5",
        "package": "prepay_id=" + pre_pay
    }
    ret_sign = sign(ret, settings.EXTRA_SETTINGS["WECHAT_SECRET"])
    ret["signType"] = ret_sign
    return ret
