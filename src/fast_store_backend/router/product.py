# -*- encoding: utf-8 -*-
"""
@File    : category.py
@Time    : 2022/10/1 22:03
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional

from fastapi import APIRouter
from starlette.requests import Request

from fast_store_backend.models import Category, Banner, Icon, Goods

router = APIRouter(prefix="/product")


@router.get("/list")
async def get_product(fid: str, tid: str):
    pass


@router.get("/cates")
async def cate_list(
    # fid: Optional[int] = None,
):
    # if fid:
    #     return await Category.filter(parent_id=fid)
    # else:
    return await Category.all()


@router.get("/banner")
async def banner_list():
    """
    首页轮播图
    """
    res = await Banner.all()
    return res


@router.get("/goods")
async def get_goods(category_id:Optional[int]=None,next: Optional[int] = None, filterIndex: Optional[str] = None):
    """
    :param next: 上次查询的最后一个id
    :param filterIndex: sales销量优先 price_min价格从小到大price_max价格从大到小
    """
    queryset = Goods.filter(status=True)
    if category_id:
        queryset=queryset.filter(category_id=category_id)
    if next:
        queryset = queryset.filter(id__gt=next)
    if filterIndex == "sales":
        queryset = queryset.order_by("-sale_num")
    elif filterIndex == "price_min":
        queryset = queryset.order_by("price")
    elif filterIndex == "price_max":
        queryset = queryset.order_by("-price")
    return await queryset.limit(100).values("image", "name", "price", "sale_num", "id")


@router.get("/icons")
async def icons(request:Request):
    return await Icon.all()


@router.get("/likes")
async def get_likes():
    return
