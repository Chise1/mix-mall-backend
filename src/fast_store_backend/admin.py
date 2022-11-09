from typing import Dict, Any, Optional, List
from fast_tmp.amis.formitem import TextItem
from fast_tmp.amis.actions import DialogAction
from fast_tmp.amis.base import _Action
from fast_tmp.amis.forms import Form
from fast_tmp.amis.frame import Dialog
from fast_store_backend.amis import SubForm
from fast_tmp.amis.view.divider import Divider
from fast_tmp.amis.wizard import Wizard, WizardStep
from fast_tmp.site.field import Password
from starlette.requests import Request

from amis_field import ColorControl
from fast_store_backend.models import Goods, GoodsSku, GoodsSpec, GoodsImage, Category, \
    CategoryType, Customer, Discuss, Banner, Icon
from fast_tmp.site import ModelAdmin
from fast_tmp.exceptions import FastTmpError


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


class GoodsAdmin(ModelAdmin):
    model = Goods
    list_display = (
        "name", "spec_type", "price", "price_line", "stock_num", "sale_num", "page_view",
        "sales_actual",
        "status",
        "image"
    )
    base_fields = (# 创建项目第一步的字段
        "category", "sn", "name", "spec_type", "status", "image")
    create_fields = (
        "category", "sn", "name", "spec_type", "price", "price_line", "sales_initial", "stock_num",
        "sale_num", "page_view",
        "sales_actual", "status", "image", "is_deleted", "desc")
    update_fields = create_fields

    def get_create_dialogation_button(self, request: Request) -> List[_Action]:
        f = self.get_create_fields()
        base_body = [f[i].get_formItem(request) for i in self.base_fields]
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
                            )
                        ],
                        api=f"post:{self.prefix}/create",
                    ),
                    actions=[],
                ),
            )
        ]


# class GoodsImageAdmin(ModelAdmin):
#     model = GoodsImage
#     list_display = ("goods", "url")
#     create_fields = list_display
#     update_fields = create_fields
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


# fixme: 只能选择一级category
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
