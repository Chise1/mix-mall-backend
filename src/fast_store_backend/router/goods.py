# -*- encoding: utf-8 -*-
"""
@File    : goods.py
@Time    : 2022/10/2 7:52
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter

router=APIRouter(prefix="/goods")

@router.get("/list")
async def get_goods_list():
    return [
        {""}
    ]