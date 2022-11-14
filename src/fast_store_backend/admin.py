import logging
import os
import time
from typing import Dict, Any, Optional, List

from fast_tmp.amis.column import Column
from fast_tmp.amis.formitem import TextItem, InputTable, ImageItem, NumberItem, UUIDItem, \
    RichTextItem
from fast_tmp.amis.actions import DialogAction
from fast_tmp.amis.base import _Action
from fast_tmp.amis.forms import Form
from fast_tmp.amis.frame import Dialog
from fast_tmp.conf import settings
from fast_tmp.responses import BaseRes
from fast_tmp.utils import remove_media_start
from pydantic import ValidationError
from tortoise import Model, transactions
from tortoise.transactions import in_transaction

from fast_store_backend.amis import SubForm
from fast_tmp.amis.wizard import Wizard, WizardStep
from fast_tmp.site.field import Password
from starlette.requests import Request

from amis_field import ColorControl, MoneyControl
from fast_store_backend.models import Goods, GoodsSku, GoodsSpec, GoodsImage, Category, \
    CategoryType, Customer, Discuss, Banner, Icon, GoodsSpecGroup
from fast_tmp.site import ModelAdmin
from fast_tmp.exceptions import FastTmpError, FieldsError

logger = logging.getLogger(__file__)


class CategoryAdmin(ModelAdmin):
    model = Category
    list_display = ("name", "code", "desc", "parent", "image")
    create_fields = list_display
    update_fields = list_display

    async def create(self, request: Request, data: Dict[str, Any]) -> Category:
        obj: Category = self.model()
        cors = []
        for field_name, field in self.get_create_fields().items():
            cor = await field.set_value(request, obj, data.get(field_name))  # 只有create可能有返回协程
            if cor:
                cors.append(cor)
        if obj.parent:
            if obj.parent.category_type == CategoryType.third:
                raise FastTmpError("深度不能超过3")
            elif obj.parent.category_type == CategoryType.second:
                obj.category_type = CategoryType.third
            else:
                obj.category_type = CategoryType.second

        await obj.save()
        for cor in cors:
            await cor
        return obj


goods_cache = {}


def set_cache(data):
    clear_cache()
    goods_cache[data["uuid"]] = (data, time.time())


def get_cache(uuid: str):
    return goods_cache.get(uuid)


def pop_cache(uuid: str):
    try:
        goods_cache.pop(uuid)
    except KeyError as e:
        logger.error("cache can not found:" + str(e))


def clear_cache():
    t = time.time()
    for k, v in goods_cache.items():
        if t - v[1] > 60 * 10:  # 缓存有效期10分钟
            goods_cache.pop(k)


class GoodsAdmin(ModelAdmin):
    model = Goods
    list_display = (
        "name", "spec_type", "price", "line_price", "stock_num", "sale_num", "page_view",
        "status",
        "image"
    )
    base_fields = (  # 创建项目第一步的字段
        "category", "name", "spec_type", "status", "image")
    create_fields = (
        "category", "name", "spec_type", "price", "line_price", "stock_num",
        "sale_num", "page_view",
        "status", "image", "is_deleted", "desc")
    update_fields = create_fields
    fields = {
        "price": MoneyControl,
        "line_price": MoneyControl
    }

    def get_create_dialogation_button(self, request: Request) -> List[_Action]:
        f = self.get_create_fields()
        base_body = [f[i].get_formitem(request) for i in self.base_fields]
        base_body.append(UUIDItem(name="uuid"))
        base_body.append(
            ImageItem(multiple=True, receiver="GoodsImage/file/url", required=True, label="商品图",
                      name="images"))
        base_body.append(SubForm(
            name="spec_group",
            label="规格组",
            multiple=True,
            btnLabel="${name}",
            visibleOn="spec_type === 'True'",
            form=Form(
                body=[
                    TextItem(
                        name="name",
                        required=True,
                        label="规格组名"
                    ),
                    SubForm(
                        name="spec",
                        label="选项",
                        multiple=True,
                        btnLabel="${value}",
                        form=Form(
                            title="增加规格选项",
                            body=[
                                TextItem(
                                    name="value",
                                    required=True,
                                    label="规格名"
                                ),
                            ]
                        )
                    )
                ]
            )
        ))
        price = f["price"].get_formitem(request)
        price.mode = "inline"
        line_price = f["line_price"].get_formitem(request)
        line_price.mode = "inline"
        stock_num = f["stock_num"].get_formitem(request)
        stock_num.mode = "inline"

        return [
            DialogAction(
                label="新增商品",
                dialog=Dialog(
                    title="新增",
                    body=Wizard(
                        steps=[
                            WizardStep(
                                title="商品基本信息",
                                body=base_body,
                                api=f"post:{self.prefix}/create",
                            ),
                            WizardStep(
                                title="商品库存",
                                body=[InputTable(
                                    name="sku",
                                    label="sku",
                                    needConfirm=False,
                                    columns=[
                                        Column(label="spec", name="spec"),
                                        ImageItem(
                                            label="封面(单规格勿传)", name="preview",
                                            receiver="GoodsSku/file/preview", required=False
                                        ),
                                        price,
                                        line_price,
                                        stock_num,
                                    ]
                                )],
                                initApi=f"get:{self.prefix}/extra/sku?" + "uuid=${uuid}",
                                initFetch=True,
                                # api=f"post:{self.prefix}/extra/sku?" + "uuid=${uuid}",
                            ), WizardStep(
                                title="商品描述",
                                body=[RichTextItem(
                                    name="desc",
                                    label="商品描述",
                                    receiver=f"{self.prefix}/extra/desc?" + "uuid=${uuid}",
                                )],
                                api=f"post:{self.prefix}/extra/sku?" + "uuid=${uuid}",
                            )
                        ],
                    ),
                    actions=[],
                ),
            )
        ]

    async def select_options(
        self,
        request: Request,
        name: str,
        pk: Optional[str],
        perPage: Optional[int],
        page: Optional[int],
    ) -> List[Dict[str, str]]:
        if name == "category":
            return await self.selct_defs[name](request, pk, perPage, page,
                                               {"category_type": CategoryType.third})
        return await self.selct_defs[name](request, pk, perPage, page, None)

    async def create(self, request: Request, data: Dict[str, Any]) -> Model:
        """
        缓存goods信息
        """
        set_cache(data)
        return

    async def router(self, request: Request, prefix: str, method: str) -> BaseRes:
        if prefix == "desc":
            # pip install aiofiles
            import aiofiles  # type: ignore
            resource = "Goods"
            body = await request.form()
            file = body.get("file")
            if not os.path.exists(settings.MEDIA_PATH):
                os.mkdir(settings.MEDIA_PATH)
            if not os.path.exists(os.path.join(settings.MEDIA_PATH, resource)):
                os.mkdir(os.path.join(settings.MEDIA_PATH, resource))
            cwd = os.path.join(settings.MEDIA_PATH, resource, prefix)
            if not os.path.exists(cwd):
                os.mkdir(cwd)
            async with aiofiles.open(os.path.join(cwd, file.filename), "wb") as f:
                await f.write(await file.read())
            res_path = f"/{settings.MEDIA_ROOT}/{resource}/{prefix}/{file.filename}"
            return BaseRes(data={"link": res_path})

        if method == "GET":
            data = get_cache(request.query_params.get("uuid"))
            if not data:
                return BaseRes(
                    msg="cache out time!",
                    status=400,
                )
            sepc_type = data[0]["spec_type"]
            if sepc_type != "True":
                return BaseRes(
                    data={"sku": [{"spec": "-", "preview": None, "price": 0, "line_price": 0,
                                   "stock_num": 0}]})

            def g(obj, tags, index) -> List[str]:
                res = []
                if index >= len(tags):
                    return [obj]
                for i in tags[index]['spec']:
                    obj2 = obj + "__" + i['value'] if len(obj) > 0 else i['value']
                    res.extend(g(obj2, tags, index + 1))
                return res

            spec_group = data[0]['spec_group']
            ret = []
            for sku in g("", spec_group, 0):
                ret.append(
                    {"spec": sku, "preview": None, "price": 0, "line_price": 0, "stock_num": 0}
                )
            return BaseRes(data={"sku": ret})
        # 真正的保存数据
        id = request.query_params.get("uuid")
        pop_cache(id)
        sku_data = await request.json()
        if sku_data["spec_type"] == "False":
            goods = Goods(
                category_id=sku_data["category"], name=sku_data["name"],
                price=sku_data['sku'][0]["price"] * 100,
                line_price=sku_data['sku'][0]["line_price"] * 100,
                stock_num=sku_data['sku'][0]["stock_num"],
                status=True if sku_data["status"] == "True" else False,
                image=remove_media_start(sku_data["image"]),
                spec_type=False,
                desc=sku_data["desc"].replace("../media",
                                              settings.EXTRA_SETTINGS["PATH"] + "/media")
            )
            async with in_transaction() as connection:
                await goods.save(using_db=connection)
                images = [GoodsImage(goods=goods, url=remove_media_start(i)) for i in
                          sku_data["images"].split(",")]
                await GoodsImage.bulk_create(images)
        else:
            line_price = 0
            price = 0
            stock_num = 0
            for sku in sku_data["sku"]:
                if sku["line_price"] > line_price:
                    line_price = sku["line_price"] * 100
                if sku["price"] < price or price == 0:
                    price = sku["price"] * 100
                stock_num += sku["stock_num"]
            goods = Goods(
                category_id=sku_data["category"], name=sku_data["name"],
                price=price,
                line_price=line_price,
                stock_num=stock_num,
                status=True if sku_data["status"] == "True" else False,
                image=remove_media_start(sku_data["image"]),
                spec_type=True,
                desc=sku_data["desc"]
            )
            async with in_transaction() as conn:
                await goods.save(conn)
                for i in sku_data['spec_group']:
                    sepc_group = GoodsSpecGroup(goods=goods, name=i['name'])
                    await sepc_group.save(conn)
                    specs = [GoodsSpec(goods=goods, spec=sepc_group, value=j['value']) for j in
                             i['spec']]
                    await GoodsSpec.bulk_create(specs)
                images = [GoodsImage(goods=goods, url=remove_media_start(i)) for i in
                          sku_data["images"].split(",")]
                await GoodsImage.bulk_create(images)
                specs = await GoodsSpec.filter(goods=goods)
                goods_skus = []
                for sku in sku_data["sku"]:
                    specList = []
                    for i in sku.pop("spec").split("__"):
                        for j in specs:
                            if j.value == i:
                                specList.append(str(j.pk))
                                break
                    specList.sort()
                    sku["preview"] = remove_media_start(sku["preview"])
                    goods_sku = GoodsSku(specs="__".join(specList), goods=goods, **sku)
                    goods_skus.append(goods_sku)
                await GoodsSku.bulk_create(goods_skus)
        return BaseRes()


class CustomerAdmin(ModelAdmin):
    model = Customer
    list_display = ("nickName", "mobile", "avatarUrl",)
    create_fields = ("nickName", "mobile", "avatarUrl",)
    update_fields = ("nickName", "mobile", "avatarUrl",)
    fields = {
        "password": Password
    }


class DiscussAdmin(ModelAdmin):
    model = Discuss
    list_display = ("customer", "nickName", "goods", "remark", "attr")
    create_fields = list_display
    update_fields = create_fields


class BannerAdmin(ModelAdmin):
    model = Banner
    list_display = ("imgUrl", "goods", "background")
    create_fields = list_display
    update_fields = list_display
    fields = {"background": ColorControl}


class IconAdmin(ModelAdmin):
    model = Icon
    list_display = ("name", "image", "category")
    create_fields = list_display
    update_fields = list_display

    async def select_options(
        self,
        request: Request,
        name: str,
        pk: Optional[str],
        perPage: Optional[int],
        page: Optional[int],
    ) -> List[Dict[str, str]]:
        if name == "category":
            res = await Category.filter(parent=None)
            return [{"label": i.name, "value": i.id} for i in res]
        else:
            return await super().select_options(request, name, pk, perPage, page)


class GoodsImageAdmin(ModelAdmin):
    model = GoodsImage
    list_display = ("goods", "url")
    create_fields = list_display
    update_fields = create_fields


class GoodsSkuAdmin(ModelAdmin):
    model = GoodsSku
    list_display = ("goods", "preview", "price", "line_price", "stock_num",)
    create_fields = list_display
    update_fields = list_display
