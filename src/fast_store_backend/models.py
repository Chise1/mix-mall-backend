import uuid
from typing import Optional

from tortoise import Model, fields
from enum import IntEnum, Enum
from fast_tmp.contrib.tortoise.fields import ImageField


class Customer(Model):
    """
    客户
    """
    nickName = fields.CharField(max_length=128, null=True, description="昵称")
    gender = fields.BooleanField(default=False, description="性别(false 为男 true为女)")
    language = fields.CharField(max_length=128, null=True, description="语言")
    city = fields.CharField(max_length=128, null=True, description="城市")
    province = fields.CharField(max_length=128, null=True, description="省")
    country = fields.CharField(max_length=128, null=True, description="国家")
    mobile = fields.CharField(max_length=32, null=True, description="手机号")
    avatarUrl = fields.CharField(max_length=255, null=True, description="头像")
    token = fields.CharField(max_length=255, null=True)
    provider = fields.CharField(max_length=255, null=True)  # 供应商？小程序？
    openid = fields.CharField(max_length=255, unique=True)
    session_key = fields.CharField(max_length=255)

    def __str__(self):
        return self.nickName


class Address(Model):
    """
    地址
    """
    name = fields.CharField(max_length=32,description="姓名")
    mobile = fields.CharField(max_length=32,description="电话")
    province = fields.CharField(max_length=32, description="省")
    city = fields.CharField(max_length=32, description="市")
    district = fields.CharField(max_length=32, description="区/县")
    address = fields.CharField(max_length=255, description="详细地址")
    isDefault = fields.BooleanField(description="是否为默认地址", default=False)
    customer = fields.ForeignKeyField("models.Customer", related_name="addresses")


class CategoryType(IntEnum):
    first = 1
    second = 2
    third = 3


class Category(Model):
    """
    商品类别
    """
    name = fields.CharField(default="", max_length=30, description="类别名", help_text="类别名")
    code = fields.CharField(default="", max_length=30, description="类别code", help_text="类别code")
    desc = fields.TextField(default="", description="类别描述", help_text="类别描述")
    parent = fields.ForeignKeyField("models.Category", related_name="children", null=True)
    children: fields.ReverseRelation['Category']
    category_type = fields.IntEnumField(CategoryType, default=CategoryType.first, null=True)
    image = ImageField(description="商品类别图片")
    # 是否放荡首页展示表
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")

    def __str__(self):
        return self.name


class Goods(Model):
    """
    商品
    """
    category = fields.ForeignKeyField("models.Category", description="商品类目")
    # sn = fields.CharField(max_length=50, default="", description="商品编码")  # 商品编码
    name = fields.CharField(max_length=30, description="商品名")
    price = fields.FloatField()  # 如果是单型号，则取这个值，如果为多型号则取下面的值
    line_price = fields.FloatField()
    stock_num = fields.IntField(description="库存总量(包含sku)")
    sale_num = fields.IntField(default=0, description="卖出数")  # 卖出数
    page_view = fields.IntField(default=0, description="浏览量")  # 卖出数
    desc = fields.TextField(description="商品详情")  # 富文本使用DjangoUeditor
    # sales_initial = fields.IntField(description="初始销量", default=0)
    # sales_actual = fields.IntField(description="实际销量", default=0)
    status = fields.BooleanField(default=False, description="是否上架")
    is_deleted = fields.BooleanField(default=False, description="是否删除")
    # sort = fields.IntField(default=9999, description="排序(数字越小越靠前)")
    image = ImageField(description="封面图片")
    # ship_free = fields.BooleanField(default=True, description="是否承担运费")  # 是否承担运费
    fav_num = fields.IntField(default=0, description="收藏数")  #
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")
    spec_type = fields.BooleanField(default=False, description="是否为多规格")

    def __str__(self):
        return self.name


class GoodsSpecGroup(Model):
    """
    商品规格组
    """
    goods = fields.ForeignKeyField("models.Goods", unique=True, db_constraint=False,
                                   related_name="spec_group")
    name = fields.CharField(max_length=255, description="规格名", )
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")

    def __str__(self):
        return self.name


class GoodsSpec(Model):
    """商品规格值"""
    spec = fields.ForeignKeyField("models.GoodsSpecGroup", related_name="valueList")
    goods = fields.ForeignKeyField("models.Goods", unique=True, db_constraint=False,
                                   related_name="specs")
    value = fields.CharField(max_length=255, description="规格值")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")

    def __str__(self):
        return self.value


class GoodsSku(Model):
    """
    商品sku
    """
    specs = fields.CharField(max_length=255, unique=True, description="商品skuid，由规格id组成")
    attrs = fields.CharField(max_length=255, description="商品attrs")
    goods = fields.ForeignKeyField("models.Goods", related_name="skus")
    preview = ImageField(max_length=255, description="预览图")
    sku_no = fields.IntField(default=1, description="商品sku编码")  # 排序用
    price = fields.FloatField()
    line_price = fields.FloatField()
    stock_num = fields.IntField(default=0, description="库存量")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")
    up_time = fields.DatetimeField(auto_now=True, description="更新时间")

    @property
    def spec_value(self):
        return [int(i) for i in self.specs.split("_")]


class GoodsImage(Model):
    """
    商品图
    """
    goods = fields.ForeignKeyField("models.Goods", related_name="images", description="商品")
    url = ImageField(description="图片")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class IndexAd(Model):
    category = fields.ForeignKeyField("models.Category", related_name='category',
                                      description="商品类目")
    goods = fields.ForeignKeyField("models.Goods", description="商品")


class HotSearchWords(Model):
    """
    热搜词
    """
    keywords = fields.CharField(default="", max_length=20, description="热搜词")
    index = fields.IntField(default=0, description="排序")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class Banner(Model):
    """
    轮播的商品
    """
    imgUrl = ImageField()
    background = fields.CharField(max_length=255)
    goods = fields.ForeignKeyField("models.Goods", description="商品", null=True)
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class Icon(Model):
    """
    首页图标
    """
    name = fields.CharField(max_length=10)
    image = ImageField()
    category = fields.ForeignKeyField("models.Category")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class Discuss(Model):
    """
    评价
    """
    customer = fields.ForeignKeyField("models.Customer", related_name="discusses")
    nickName = fields.CharField(max_length=128)  # 绑定customer的名字
    goods = fields.ForeignKeyField("models.Goods", description="商品")
    remark = fields.TextField()
    attrs = fields.CharField(max_length=255, null=True)
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class GoodsHistory(Model):
    """
    浏览历史记录
    """
    goods = fields.ForeignKeyField("models.Goods", db_constraint=False, related_name="history")
    customer = fields.ForeignKeyField("models.Customer", db_constraint=False,
                                      related_name="history")
    add_time = fields.DatetimeField(description="浏览时间")
    favorite = fields.BooleanField(default=False, description="收藏")

    class Meta:
        unique_together = (("goods", "customer"),)


class Cart(Model):
    """
    购物车
    """
    goods: Goods = fields.ForeignKeyField("models.Goods", db_constraint=False)
    sku: Optional[GoodsSku] = fields.ForeignKeyField(
        "models.GoodsSku", db_constraint=False, null=True)
    number = fields.IntField(default=0, description="数量")
    customer = fields.ForeignKeyField("models.Customer", db_constraint=False)
    add_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("goods", "sku", "customer"),)


class OrderSub(Model):
    """
    订单子项
    """
    order = fields.ForeignKeyField(
        "models.Order", related_name="goodsList", description="订单"
    )
    goods: Goods = fields.ForeignKeyField("models.Goods", db_constraint=False)
    sku: Optional[GoodsSku] = fields.ForeignKeyField(
        "models.GoodsSku", db_constraint=False, null=True)
    price = fields.FloatField()
    preview = fields.CharField(max_length=255, description="商品图片")
    name = fields.CharField(max_length=255, description="商品名")
    attrs = fields.CharField(max_length=255, description="商品attrs")
    number = fields.IntField(default=0, description="数量")
    add_time = fields.DatetimeField(auto_now_add=True)
    stock_num = fields.IntField(default=0, description="库存量")


class OrderState(IntEnum):
    """
    订单状态
    """
    notpay = 1  # 待支付
    unreceipted = 2  # 待发货
    receipted = 3  # 待收货
    discuss = 4  # 待评价
    cancel = 9  # 取消订单
    # todo 退货流程？？


class LogisticsType(IntEnum):
    """
    配送方式
    0=无需配送 1=快递 2=商家 3=同城 4=自提
    """
    not_need = 0
    courier = 1
    merchant = 2
    intra_city = 3
    customer_self = 4


def get_trade_no():
    return str(uuid.uuid4()).replace("-", "")


class Order(Model):
    """
    订单
    """
    trade_no = fields.CharField(default=get_trade_no, max_length=32, unique=True, description="订单号")
    customer = fields.ForeignKeyField("models.Customer", db_constraint=False)
    price = fields.FloatField(description="总的支付金额")
    state = fields.IntEnumField(OrderState, default=OrderState.notpay, description="订单状态")
    pay_no = fields.CharField(null=True, max_length=128, description="支付流水号")
    logistics_type = fields.IntEnumField(LogisticsType, default=LogisticsType.not_need)
    remark = fields.CharField(max_length=255, description="备注")
    add_time = fields.DatetimeField(auto_now_add=True)
    address = fields.JSONField()
