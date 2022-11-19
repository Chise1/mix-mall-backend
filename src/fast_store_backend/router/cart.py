from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from fast_store_backend.dantic_model import CartGoods, CartAdd
from fast_store_backend.depends import get_customer
from fast_store_backend.models import Customer, Cart

router = APIRouter(prefix="/cart", tags=["购物车"])


@router.get("/goods", response_model=List[CartGoods])
async def get_cart(customer: Customer = Depends(get_customer)):
    """
    购物车
    """
    cart_list = await Cart.filter(customer=customer).prefetch_related("goods", "sku")
    ret = []
    for cart in cart_list:
        if cart.sku:
            ret.append({
                "goods": {
                    "id": cart.goods.pk,
                    "image": cart.sku.preview,
                    "attrs": cart.sku.attrs,
                    "name": cart.goods.name,
                    "price": cart.sku.price,
                    "line_price": cart.sku.line_price,
                    "sku_id": cart.sku.pk
                },
                "number": cart.number,
                "id": cart.pk
            })
        else:
            ret.append({
                "goods": {
                    "id": cart.goods.pk,
                    "image": cart.goods.image,
                    "attrs": "-",
                    "name": cart.goods.name,
                    "price": cart.goods.price,
                    "line_price": cart.goods.line_price,
                    "sku_id": None
                },
                "number": cart.number,
                "id": cart.pk
            })
    return ret


@router.delete("/goods/clear")
async def clear_cart(customer: Customer = Depends(get_customer)):
    """
    清空购物车
    """
    await Cart.filter(customer=customer).delete()


@router.delete("/goods/remove")
async def remove_cart(cart_id: int, customer: Customer = Depends(get_customer)):
    """
    删除购物车商品
    """
    await Cart.filter(pk=cart_id, customer=customer).delete()


@router.post("/goods")
async def add_cart(cartinfo: CartAdd, customer: Customer = Depends(get_customer)):
    """
    加入购物车
    """
    cart = await Cart.filter(
        goods_id=cartinfo.goods_id, sku_id=cartinfo.sku_id, customer=customer).first()
    if not cart:
        cart = Cart(goods_id=cartinfo.goods_id, sku_id=cartinfo.sku_id, customer=customer)
    cart.number += cartinfo.number
    await cart.save()


@router.post("/number")
async def add_cart_number(cart_id: int, number: int, customer: Customer = Depends(get_customer)):
    """
    修改商品数量
    """
    if number < 0:
        number = 0
    await Cart.filter(pk=cart_id, customer=customer).update(number=number)
