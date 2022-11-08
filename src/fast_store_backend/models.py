from tortoise import Model, fields
from enum import IntEnum
from fast_tmp.contrib.tortoise.fields import ImageField


class Customer(Model):
    username = fields.CharField(max_length=128, unique=True)
    password = fields.CharField(max_length=255)
    nickName = fields.CharField(max_length=128)
    phone = fields.CharField(32)
    imgUrl = ImageField()
    token = fields.CharField(max_length=255, null=True)
    provider = fields.CharField(max_length=255, null=True)  # 供应商？
    openid = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nickName


class Address(Model):
    name = fields.CharField(max_length=32)
    mobile = fields.CharField(max_length=32)
    province = fields.CharField(max_length=32, description="省")
    city = fields.CharField(max_length=32, description="市")
    district = fields.CharField(max_length=32, description="区")
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
    parent = fields.ForeignKeyField("models.Category", related_name="childs", null=True)
    category_type = fields.IntEnumField(CategoryType, default=CategoryType.first, null=True)
    image = ImageField()
    # 是否放荡首页展示表
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")

    def __str__(self):
        return self.name


class Goods(Model):
    """
    商品
    """
    category = fields.ForeignKeyField("models.Category", description="商品类目")
    sn = fields.CharField(max_length=50, default="", description="商品编码")  # 商品编码
    name = fields.CharField(max_length=30, description="商品名")
    price = fields.IntField()  # 如果是单型号，则取这个值，如果为多型号则取下面的值
    price_line = fields.IntField()
    line_price_min = fields.IntField(default=0)
    line_price_max = fields.IntField(default=0)
    stock_num = fields.IntField(description="库存总量(包含sku)")
    sale_num = fields.IntField(default=0, description="卖出数")  # 卖出数
    page_view = fields.IntField(default=0, description="浏览量")  # 卖出数
    desc = fields.TextField(description="商品详情")  # 富文本使用DjangoUeditor
    sales_initial = fields.IntField(description="初始销量", default=0)
    sales_actual = fields.IntField(description="实际销量", default=0)
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
    goods = fields.ForeignKeyField("models.Goods", db_constraint=False)
    name = fields.CharField(max_length=255, description="规格名")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class GoodsSpec(Model):
    """商品规格值"""
    spec = fields.ForeignKeyField("models.GoodsSpecGroup", related_name="valueList")
    value = fields.CharField(max_length=255, description="规格值")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class GoodsSku(Model):
    """
    商品sku
    """
    sku_id = fields.CharField(max_length=255, unique=True, description="商品skuid，由规格id组成")
    goods = fields.ForeignKeyField("models.Goods", )
    preview = fields.CharField(max_length=255, description="预览图")
    sku_no = fields.CharField(max_length=255, description="商品sku编码")  # 排序用
    price = fields.IntField()
    line_price = fields.IntField()
    stock_num = fields.IntField(default=0, description="库存量")
    # 减少查询商品的时候的查询次数？
    # sku_props = fields.CharField(max_length=255, description="SKU的规格属性(json格式)")
    # sepc_values = fields.CharField(max_length=255, description="规格值ID集(json格式)")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")
    up_time = fields.DatetimeField(auto_now=True, description="更新时间")

    @property
    def spec_value(self):
        return [int(i) for i in self.sku_id.split("_")]


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


class TopBar(Model):
    """
    首页分类
    """
    name = fields.CharField(max_length=32)
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class IndexInfo(Model):
    goods = fields.ForeignKeyField("models.Goods", description="商品")
    imgUrl = fields.CharField(max_length=255, description="轮播图片")
    index = fields.IntField(default=0, description="轮播顺序")
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")

    class Meta:
        abstract = True


class Swiper(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="swiperList")


class Recommend(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="recommendList")


class Commdity(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="commdityList")


class Banner(IndexInfo):
    """
    轮播的商品
    """
    imgUrl = ImageField()
    background = fields.CharField(max_length=255)
    goods = fields.ForeignKeyField("models.Goods", description="商品", null=True)
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")


class Card(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="cardList")


class Hot(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="hotList")


class Shop(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="shopList")


class Icons(IndexInfo):
    topBar = fields.ForeignKeyField("models.TopBar", related_name="icons")


class Discuss(Model):
    """
    评价
    """
    customer = fields.ForeignKeyField("models.Customer", related_name="discusses")
    goods = fields.ForeignKeyField("models.Goods", description="商品")
    remark = fields.TextField()
    attr = fields.CharField(max_length=255, null=True)
    add_time = fields.DatetimeField(auto_now_add=True, description="添加时间")
