"""
接口请求和返回的数据结构
"""
from typing import Optional, List

from pydantic import BaseModel, Field


class Goods(BaseModel):
    id: int
    image: str
    attrs: str
    name: str
    price: int
    line_price: int
    sku_id: Optional[int]


class CartGoods(BaseModel):
    number: int = Field(..., description="数量")
    id: int = Field(..., description="购物车id")
    goods: Goods = Field(..., description="商品信息")


class CartAdd(BaseModel):
    """
    增加购物车
    """
    goods_id: int
    sku_id: Optional[int]
    number: int


class OrderGoodsInfo(BaseModel):
    sku_id: Optional[int]
    goods_id: int
    num: int
    cart_id: Optional[int]


class CreateOrderInfo(BaseModel):
    """
    创建订单
    """
    address: dict  # todo
    goodsList: List[OrderGoodsInfo]
    remark: str
