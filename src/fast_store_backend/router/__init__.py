# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2022/10/1 17:21
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fast_store_backend.router.product import router as category_router
from fast_store_backend.router.cart import router as cart_router
from fast_store_backend.router.user import router as auth_router
from fast_store_backend.router.goods import router as goods_router
from fast_store_backend.router.pay import router as pay_router
from fastapi import APIRouter

default_router = APIRouter()

default_router.include_router(category_router)
default_router.include_router(cart_router)
default_router.include_router(auth_router)
default_router.include_router(goods_router)
default_router.include_router(pay_router)
