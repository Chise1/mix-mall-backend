import json
from typing import Optional
import aiohttp
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from fast_store_backend.depends import get_customer, get_customer_or_none, create_token
from fast_store_backend.models import Customer, Goods, Address, GoodsHistory

router = APIRouter(prefix="/user")


@router.get("/addresses")
async def get_address(customer: Customer = Depends(get_customer)):
    return await Address.filter(customer=customer)


class CreateAddress(BaseModel):
    id: Optional[int] = None
    name: str
    mobile: str
    address: str
    defalut: bool = False


@router.post("/address")
async def create_address(info: CreateAddress):
    return info


@router.get("/userInfo")
async def userinfo(customer: Customer = Depends(get_customer)):
    """
    读取客户信息
    """
    ret = dict(customer)
    ret.pop("password")
    ret.pop("username")
    return ret


@router.get("/view_history")
async def get_user_view_history(customer: Customer = Depends(get_customer_or_none)):
    """
    获取客户浏览历史记录
    """
    if not customer:
        return {}
    return await Goods.filter(history__customer=customer).order_by("-history__add_time").limit(
        10).values("id", "name", "image", "history__add_time")


@router.get("/loginByWeixin")
async def wechat_login(request: Request, code: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.weixin.qq.com/sns/jscode2session?appid=wx833cac1c9bdff8b1&secret=23fa3107719720aeda71b2b3441bfe66&js_code={code}&grant_type=authorization_code")
        data = json.loads(await response.text())
        openid = data.get("openid")
        print(data)
        if not openid:
            return JSONResponse(content={"msg": data["errmsg"], "status": 400},
                                status_code=status.HTTP_400_BAD_REQUEST)
        customer = await Customer.filter(openid=openid).first()
        if not customer:
            customer = Customer(**data)
            await customer.save()
            return {"token": create_token(customer), "registered": False}
        return {"token": create_token(customer), "registered": True}


@router.post("/userInfo")
async def update_userInfo(request: Request, customer: Customer = Depends(get_customer)):
    data = await request.json()  # {'nickName': '微信用户', 'gender': 0, 'language': '', 'city': '', 'province': '', 'country': '', 'avatarUrl': 'https://thirdwx.qlogo.cn/mmopen/vi_32/POgEwh4mIHO4nibH0KlMECNjjGxQUq24ZEaGT4poC6icRiccVGKSyXwibcPq4BWmiaIGuG1icwxaQX6grC9VemZoJ8rg/132'}
    customer.nickName = data["nickName"]
    await customer.update_from_dict(data)
    return


@router.post("/favorite")
async def favorite(goods_id: int, favorite: bool, customer: Customer = Depends(get_customer)):
    """
    收藏或取消收藏
    """
    await GoodsHistory.filter(goods_id=goods_id, customer=customer).update(favorite=favorite)
    return {"favorite": favorite}
