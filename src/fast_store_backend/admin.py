import time
from typing import Dict, Any, Optional, List

from fast_tmp.amis.column import Column
from fast_tmp.amis.formitem import TextItem, InputTable, ImageItem, NumberItem, UUIDItem
from fast_tmp.amis.actions import DialogAction
from fast_tmp.amis.base import _Action
from fast_tmp.amis.forms import Form
from fast_tmp.amis.frame import Dialog
from fast_tmp.responses import BaseRes
from tortoise import Model, transactions
from tortoise.exceptions import ValidationError

from fast_store_backend.amis import SubForm
from fast_tmp.amis.wizard import Wizard, WizardStep
from fast_tmp.site.field import Password
from starlette.requests import Request

from amis_field import ColorControl
from fast_store_backend.models import Goods, GoodsSku, GoodsSpec, GoodsImage, Category, \
    CategoryType, Customer, Discuss, Banner, Icon
from fast_tmp.site import ModelAdmin
from fast_tmp.exceptions import FastTmpError, FieldsError


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


def clear_cache():
    t = time.time()
    for k, v in goods_cache.items():
        if t - v[1] > 60 * 10:  # 缓存有效期10分钟
            goods_cache.pop(k)


class GoodsAdmin(ModelAdmin):
    model = Goods
    list_display = (
        "name", "spec_type", "price", "line_price", "stock_num", "sale_num", "page_view",
        "sales_actual",
        "status",
        "image"
    )
    base_fields = (  # 创建项目第一步的字段
        "category", "name", "spec_type", "status", "image")
    create_fields = (
        "category", "name", "spec_type", "price", "line_price", "sales_initial", "stock_num",
        "sale_num", "page_view",
        "sales_actual", "status", "image", "is_deleted", "desc")
    update_fields = create_fields

    def get_create_dialogation_button(self, request: Request) -> List[_Action]:
        f = self.get_create_fields()
        base_body = [f[i].get_formitem(request) for i in self.base_fields]
        base_body.append(UUIDItem(name="uuid"))
        base_body.append(
            ImageItem(multiple=True, receiver="GoodsImage/file/url", label="商品图", name="images"))
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
                                debug=True,
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
                                        f["price"].get_formitem(request),
                                        f["line_price"].get_formitem(request),
                                        f["stock_num"].get_formitem(request),
                                    ]
                                )],
                                initApi=f"get:{self.prefix}/extra/sku?" + "uuid=${uuid}",
                                initFetch=True,
                                api=f"post:{self.prefix}/extra/sku",
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
        obj = self.model()
        cors = []
        field_errors = {}
        for field_name, field in self.get_create_fields().items():
            try:
                cor = await field.set_value(request, obj, data.get(field_name))  # 只有create可能有返回协程
                if cor:
                    cors.append(cor)
            except ValidationError as e:
                field_errors[field_name] = str(e)
        if field_errors:
            raise FieldsError(field_errors)

        @transactions.atomic()
        async def save_all():
            await obj.save()
            for cor in cors:
                await cor

        await save_all()
        return obj

    async def router(self, request: Request, prefix: str, method: str) -> BaseRes:
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
        x = await request.json()
        print(x)
        return BaseRes()


class CustomerAdmin(ModelAdmin):
    model = Customer
    list_display = ("nickName", "username", "phone", "imgUrl",)
    create_fields = ("nickName", "username", "password", "phone", "imgUrl",)
    update_fields = ("nickName", "username", "password", "phone", "imgUrl",)
    fields = {
        "password": Password
    }


class DiscussAdmin(ModelAdmin):
    model = Discuss
    list_display = ("customer", "goods", "remark", "attr")
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
