# -*- encoding: utf-8 -*-
"""
@File    : goods.py
@Time    : 2022/10/2 7:52
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from typing import Optional

from fastapi import APIRouter

from fast_store_backend.models import Discuss, Goods, GoodsSpecGroup, GoodsSku

router = APIRouter(prefix="/goods", tags=["goods"])


@router.get("/list")
async def get_goods_list():
    return [
        {""}
    ]


@router.get("/detail/{id}")
async def get_goods_detail(id: int):
    """
    获取细节
    """
    goods = await Goods.filter(pk=id, status=True).prefetch_related("images").first()

    ret = {
        "id": id,
        "name": goods.name,
        "favorite": True,  # 是否已经收藏
        "spec_type": goods.spec_type,  # 商品规格，单规格还是多规格
        "price": goods.price / 100,  # 热销产品折后价格
        "line_price": goods.line_price / 100,
        "stock_num": goods.stock_num,  # 总库存
        "sale_num": goods.sale_num,  # 总销量
        "page_view": goods.page_view,  # 浏览量
        "desc": goods.desc,
        "status": goods.status,  # false为下架
        "images": [
            {"id": i.id,
             "url": i.url} for i in goods.images],
        "image": goods.image
    }

    remark = await Discuss.filter(goods=goods).first()
    if remark:
        remark_total = await Discuss.filter(goods=goods).count()
        ret["remark"] = {
            "total": remark_total,
            "id": remark.pk,
            "name": remark.nickName,
            "remark": remark.remark,
            "attr": remark.attr,
            "add_time": remark.add_time.strftime("%Y-%m-%d %H:%M:%S")
        }
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
             "spec_value": [int(i) for i in sku.specs.split("__")]
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
