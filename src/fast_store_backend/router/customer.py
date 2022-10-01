# -*- encoding: utf-8 -*-
"""
@File    : customer.py
@Time    : 2022/10/1 23:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter

router = APIRouter(prefix="/customer")


@router.get("/cart")
async def get_cart():
    return [{
        "id": 1,
        "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553005139&di=3368549edf9eee769a9bcb3fbbed2504&imgtype=jpg&er=1&src=http%3A%2F%2Fimg002.hc360.cn%2Fy3%2FM01%2F5F%2FDB%2FwKhQh1T7iceEGRdWAAAAADQvqk8733.jpg',
        "attr_val": '春装款 L',
        "stock": 15,
        "title": 'OVBE 长袖风衣',
        "price": 278.00,
        "number": 1
    },
        {
            "id": 3,
            "image": 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2319343996,1107396922&fm=26&gp=0.jpg',
            "attr_val": '激光导航 扫拖一体',
            "stock": 3,
            "title": '科沃斯 Ecovacs 扫地机器人',
            "price": 1348.00,
            "number": 5
        },
        {
            "id": 4,
            "image": 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2668268226,1765897385&fm=26&gp=0.jpg',
            "attr_val": 'XL',
            "stock": 55,
            "title": '朵绒菲小西装',
            "price": 175.88,
            "number": 1
        },
        {
            "id": 5,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1552410549432&di=06dd3758053fb6d6362516f30a42d055&imgtype=0&src=http%3A%2F%2Fimgcache.mysodao.com%2Fimg3%2FM0A%2F67%2F42%2FCgAPD1vNSsHNm-TnAAEy61txQb4543_400x400x2.JPG',
            "attr_val": '520 #粉红色',
            "stock": 15,
            "title": '迪奥（Dior）烈艳唇膏',
            "price": 1089.00,
            "number": 1
        },
        {
            "id": 6,
            "image": 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1031875829,2994442603&fm=26&gp=0.jpg',
            "attr_val": '樱花味润手霜 30ml',
            "stock": 15,
            "title": "欧舒丹（L'OCCITANE）乳木果",
            "price": 128,
            "number": 1
        },
        {
            "id": 7,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553007107&di=390915aa8a022cf0b03c03340881b0e7&imgtype=jpg&er=1&src=http%3A%2F%2Fimg13.360buyimg.com%2Fn0%2Fjfs%2Ft646%2F285%2F736444951%2F480473%2Faa701c97%2F548176feN10c9ed7b.jpg',
            "attr_val": '特级 12个',
            "stock": 7,
            "title": '新疆阿克苏苹果 特级',
            "price": 58.8,
            "number": 10
        },
        {
            "id": 8,
            "image": 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2319343996,1107396922&fm=26&gp=0.jpg',
            "attr_val": '激光导航 扫拖一体',
            "stock": 15,
            "title": '科沃斯 Ecovacs 扫地机器人',
            "price": 1348.00,
            "number": 1
        },
        {
            "id": 9,
            "image": 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=2668268226,1765897385&fm=26&gp=0.jpg',
            "attr_val": 'XL',
            "stock": 55,
            "title": '朵绒菲小西装',
            "price": 175.88,
            "number": 1
        },
        {
            "id": 10,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1552410549432&di=06dd3758053fb6d6362516f30a42d055&imgtype=0&src=http%3A%2F%2Fimgcache.mysodao.com%2Fimg3%2FM0A%2F67%2F42%2FCgAPD1vNSsHNm-TnAAEy61txQb4543_400x400x2.JPG',
            "attr_val": '520 #粉红色',
            "stock": 15,
            "title": '迪奥（Dior）烈艳唇膏',
            "price": 1089.00,
            "number": 1
        },
        {
            "id": 11,
            "image": 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1031875829,2994442603&fm=26&gp=0.jpg',
            "attr_val": '樱花味润手霜 30ml',
            "stock": 15,
            "title": "欧舒丹（L'OCCITANE）乳木果",
            "price": 128,
            "number": 1
        },
        {
            "id": 12,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553007107&di=390915aa8a022cf0b03c03340881b0e7&imgtype=jpg&er=1&src=http%3A%2F%2Fimg13.360buyimg.com%2Fn0%2Fjfs%2Ft646%2F285%2F736444951%2F480473%2Faa701c97%2F548176feN10c9ed7b.jpg',
            "attr_val": '特级 12个',
            "stock": 7,
            "title": '新疆阿克苏苹果 特级',
            "price": 58.8,
            "number": 10
        },
        {
            "id": 13,
            "image": 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1552405266625&di=a703f2b2cdb0fe7f3f05f62dd91307ab&imgtype=0&src=http%3A%2F%2Fwww.78.cn%2Fzixun%2Fnews%2Fupload%2F20190214%2F1550114706486250.jpg',
            "attr_val": '春装款/m',
            "stock": 15,
            "title": '女装2019春秋新款',
            "price": 420.00,
            "number": 1
        }
    ]
