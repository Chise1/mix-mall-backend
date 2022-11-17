# -*- encoding: utf-8 -*-
"""
@File    : goods.py
@Time    : 2022/10/2 7:52
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import asyncio
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import BackgroundTasks
from tortoise.expressions import F

from fast_store_backend.depends import get_customer_or_none
from fast_store_backend.models import Discuss, Goods, GoodsSpecGroup, GoodsSku, Customer, \
    GoodsHistory

router = APIRouter(prefix="/goods", tags=["goods"])


@router.get("/list")
async def get_goods_list():
    return [
        {""}
    ]


async def add_history(history: Optional[GoodsHistory], customer: Optional[Customer], goods_id: int):
    """
    增加记录
    :param history:
    :param customer:
    :return:
    """
    if history:
        history.add_time = datetime.now()
        await history.save()
    else:
        if customer:
            await GoodsHistory.create(
                goods_id=goods_id,
                customer=customer,
                add_time=datetime.now()
            )
    await Goods.filter(pk=goods_id).update(page_view=F("page_view") + 1)


async def add_page_view(goods_id: int, ret: dict, customer: Optional[Customer],
                        background_tasks: BackgroundTasks):
    if customer:
        history = await GoodsHistory.filter(goods_id=goods_id, customer=customer).first()
        if history:
            ret['favorite'] = history.favorite
        background_tasks.add_task(add_history, history, customer, goods_id)
    else:
        background_tasks.add_task(add_history, None, customer, goods_id)


async def get_remark(ret: dict, goods_id: int):
    remark = await Discuss.filter(goods_id=goods_id).first()
    if remark:
        remark_total = await Discuss.filter(goods_id=goods_id).count()
        ret["remark"] = {
            "total": remark_total,
            "id": remark.pk,
            "name": remark.nickName,
            "remark": remark.remark,
            "attrs": remark.attrs,
            "add_time": remark.add_time.strftime("%Y-%m-%d %H:%M:%S")
        }


async def get_goods(ret: dict, goods_id: int):
    goods = await Goods.filter(pk=goods_id, status=True).prefetch_related("images").first()
    ret.update(**{
        "id": goods_id,
        "name": goods.name,
        "spec_type": goods.spec_type,  # 商品规格，单规格还是多规格
        "price": goods.price ,  # 热销产品折后价格
        "line_price": goods.line_price ,
        "stock_num": goods.stock_num,  # 总库存
        "sale_num": goods.sale_num,  # 总销量
        "page_view": goods.page_view,  # 浏览量
        "desc": goods.desc,
        "status": goods.status,  # false为下架
        "images": [
            {"id": i.id,
             "url": i.url} for i in goods.images],
        "image": goods.image
    })
    if goods.spec_type:
        spec_group = await GoodsSpecGroup.filter(goods=goods).prefetch_related("valueList")
        skus = await GoodsSku.filter(goods=goods)
        ret["specList"] = [
            {"id": i.pk, "name": i.name, "valueList": [
                {"id": j.pk, "value": j.value}
                for j in i.valueList
            ]}
            for i in spec_group]
        ret["skuList"] = [
            {"id": sku.pk,
             "sku_id": sku.specs,
             "sku_no": 1,  # 排序用
             "price": sku.price,
             "line_price": sku.line_price,
             "stock_num": sku.stock_num,
             "preview": sku.preview,
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [int(i) for i in sku.specs.split("__")],
             "attrs":sku.attrs
             }
            for sku in skus
        ]
    else:
        ret["specList"] = [
            {"id": 0, "name": "选择", "valueList": [
                {"id": 0, "value": goods.name}
            ]}]
        ret["skuList"] = [
            {"id": goods.pk,
             "sku_id": "0",
             "sku_no": 1,  # 排序用
             "price": goods.price,
             "line_price": goods.line_price,
             "stock_num": goods.stock_num,
             "preview": goods.image,
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [0]
             }
        ]


# fixme: 可以作为教程
@router.get("/detail/{id}")
async def get_goods_detail(
    id: int,
    background_tasks: BackgroundTasks,
    customer: Optional[Customer] = Depends(get_customer_or_none),
):
    """
    获取商品细节
    """
    ret = {"favorite":False}
    await asyncio.gather(  # 同步执行
        add_page_view(id, ret, customer, background_tasks),
        get_goods(ret, id),
        get_remark(ret, id)
    )
    return ret


@router.get("/detail/{goods_id}/remark")
async def get_remarks(
    goods_id: int,
    next: int = 0
):
    """
    评价
    """
    discusses = await Discuss.filter(goods_id=goods_id, id__gt=next).select_related(
        "customer").order_by("add_time").values("customer", "remark", "attr", "add_time")
    return {
        "next": 11,
        "data": [{
            "id": 1,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "avatar": "https://gd4.alicdn.com/imgextra/i4/479184430/O1CN01tWg4Us1iaz4auqelt_!!479184430.jpg_400x400.jpg",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 2,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 3,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 4,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 5,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 6,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 7,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 8,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 9,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }, {
            "id": 10,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }]
    }
