# -*- encoding: utf-8 -*-
"""
@File    : index.py
@Time    : 2022/10/1 17:22
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter

# from fast_store_backend.models import TopBar

router = APIRouter()

#
# @router.get("/index/data")
# async def index_list():
#     topBar_list = await TopBar.all()
#     default = await TopBar.all().prefetch_related("swpiers").first()  # 默认
#     return {
#         "type": "recommendList",
#         "data": [
#             {
#                 "bigUrl": ".../ddd",
#                 "data": [
#                     {"imgUrl": "dd"}
#                 ]
#             }
#         ]
#     }
