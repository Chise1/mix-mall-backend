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

from fast_store_backend.models import Discuss

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
    :param id:
    """
    return {
        "id": id,
        "name": "荣耀 V10全网通 标配版 4GB+64GB 魅丽红 移动联通电信4G全面屏手机 双卡双待",
        "favorite": True,  # 是否已经收藏
        # "no": "",
        "spec_type": True,  # 商品规格，单规格还是多规格
        "price": "350.00",  # 热销产品折后价格
        "line_price_min": "300.00",  # 划线价格
        "line_price_max": "400.00",
        "stock_num": 690,  # 总库存
        "sale_num": 100,  # 总销量
        "page_view": 888,  # 浏览量
        "desc": """<div style="width:100%">
							<img style="width:100%;display:block;" src="https://gd3.alicdn.com/imgextra/i4/479184430/O1CN01nCpuLc1iaz4bcSN17_!!479184430.jpg_400x400.jpg" />
							<img style="width:100%;display:block;" src="https://gd2.alicdn.com/imgextra/i2/479184430/O1CN01gwbN931iaz4TzqzmG_!!479184430.jpg_400x400.jpg" />
							<img style="width:100%;display:block;" src="https://gd3.alicdn.com/imgextra/i3/479184430/O1CN018wVjQh1iaz4aupv1A_!!479184430.jpg_400x400.jpg" />
							<img style="width:100%;display:block;" src="https://gd4.alicdn.com/imgextra/i4/479184430/O1CN01tWg4Us1iaz4auqelt_!!479184430.jpg_400x400.jpg" />
							<img style="width:100%;display:block;" src="https://gd1.alicdn.com/imgextra/i1/479184430/O1CN01Tnm1rU1iaz4aVKcwP_!!479184430.jpg_400x400.jpg" />
						</div>""",
        "status": True,  # false为下架
        "images": [
            {"id": 1,
             "url": 'https://gd3.alicdn.com/imgextra/i3/0/O1CN01IiyFQI1UGShoFKt1O_!!0-item_pic.jpg_400x400.jpg'},
            {"id": 2,
             "url": 'https://gd3.alicdn.com/imgextra/i3/TB1RPFPPFXXXXcNXpXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg'},
            {"id": 3,
             "url": 'https://gd2.alicdn.com/imgextra/i2/38832490/O1CN01IYq7gu1UGShvbEFnd_!!38832490.jpg_400x400.jpg'},
        ],
        "image": "http:\/\/static.yoshop.xany6.com\/2018071718294208f086786.jpg",
        "specList": [
            {"id": 10001, "name": "颜色", "valueList": [
                {"id": 10044, "value": "炫影蓝"},
                {"id": 10045, "value": "沙滩金"}
            ]},
            {"id": 10002, "name": "版本", "valueList": [
                {"id": 10047, "value": "4+64G"},
                {"id": 10048, "value": "6+128G"}]
             }
        ],
        "skuList": [
            {"id": 10124,
             "sku_id": "10044_10047",
             "goods_id": 10015,
             "sku_no": 1,  # 排序用
             "price": "1899.00",
             "line_price": "0.00",
             "stock_num": 90,
             "preview": "http://static.yoshop.xany6.com/201807171829416962a0585.jpg",
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [10044, 10047]
             },
            {"id": 10125,
             "sku_id": "10044_10048",
             "goods_id": 10015,
             "sku_no": 2,
             "price": "1899.00",
             "line_price": "0.00",
             "stock_num": 100,
             "preview": "http://static.yoshop.xany6.com/201807171829416962a0585.jpg",
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [10044, 10048]
             },
            {"id": 10126,
             "sku_id": "10045_10047",
             "goods_id": 10015,
             "sku_no": 2,
             "price": "1899.00",
             "line_price": "0.00",
             "stock_num": 110,
             "preview": "http://static.yoshop.xany6.com/201807171829416962a0585.jpg",
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [10045, 10047]
             },
            {"id": 10127,
             "sku_id": "10045_10048", "goods_id": 10015,
             "sku_no": 4,
             "price": "400.00",
             "line_price": "410.00",
             "stock_num": 120,
             "preview": "http://static.yoshop.xany6.com/201807171829416962a0585.jpg",
             "preview_id": None,  # 如果没有preview从这里读取，然后进行判断。
             "spec_value": [10045, 10048]
             }
        ],
        "remark": {
            "total": 86,
            "id": 7,
            "name": "leo yo",
            "remark": "商品收到了，79元两件，质量不错，试了一下有点瘦，但是加个外罩很漂亮，我很喜欢",
            "attr": "购买类型：XL 红色",
            "add_time": "2019-04-01 19:21"
        }
    }


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
