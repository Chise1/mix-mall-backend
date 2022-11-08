from fastapi import APIRouter

router = APIRouter(prefix="/customer")


@router.get("/cart")
async def get_cart():
    """
    购物车
    """
    return [{
        "goods": {
            "id": 1,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553005139&di=3368549edf9eee769a9bcb3fbbed2504&imgtype=jpg&er=1&src=http%3A%2F%2Fimg002.hc360.cn%2Fy3%2FM01%2F5F%2FDB%2FwKhQh1T7iceEGRdWAAAAADQvqk8733.jpg',
            "attr_val": '春装款 L',
            "stock": 15,
            "title": 'OVBE 长袖风衣',
            "price": 278.00,
        },
        "number": 1,
        "id": 1
    }, {
        "goods": {
            "id": 2,
            "image": 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2319343996,1107396922&fm=26&gp=0.jpg',
            "attr_val": '激光导航 扫拖一体',
            "stock": 3,
            "title": '科沃斯 Ecovacs 扫地机器人',
            "price": 1348.00,
        },
        "number": 1,
        "id": 2
    }, {
        "goods": {
            "id": 3,
            "image": 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2668268226,1765897385&fm=26&gp=0.jpg',
            "attr_val": 'XL',
            "stock": 55,
            "title": '朵绒菲小西装',
            "price": 175.88
        },
        "number": 1,
        "id": 3
    }]


@router.delete("/cart/clear")
async def clear_cart():
    """
    清空购物车
    """
    return
@router.post("/cart")
async def add_to_cart():
    """
    加入购物车
    """

@router.post("/goods/favorite/{id}")
async def collect_goods(id: int):
    """
    收藏
    """
    return {
        "data": True
    }


@router.get("/goods/favorite/{id}")
async def collect_goods(id: int):
    """
    收藏
    """
    return {
        "data": True
    }
