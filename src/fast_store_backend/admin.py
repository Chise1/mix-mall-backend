from typing import Dict, Any

from fast_tmp.site.field import Password
from starlette.requests import Request

from amis_field import ColorControl
from fast_store_backend.models import Goods, GoodsSku, GoodsSpec, GoodsImage, Category, \
    CategoryType, Customer, Discuss, Banner
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
        "image")
    create_fields = (
        "category", "sn", "name", "spec_type", "price", "price_line", "sales_initial", "stock_num",
        "sale_num", "page_view",
        "sales_actual", "status", "image", "is_deleted", "desc")
    update_fields = create_fields


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
