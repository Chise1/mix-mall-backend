from tortoise import Model, fields


class Customer(Model):
    username = fields.CharField(max_length=128, unique=True)
    password = fields.CharField(max_length=255)
    nickName = fields.CharField(max_length=128)
    phone = fields.CharField(32)
    imgUrl = fields.CharField(max_length=255)
    token = fields.CharField(max_length=255)
    provider = fields.CharField(max_length=255)  # 供应商？
    openid = fields.CharField(max_length=255)


class Address(Model):
    name = fields.CharField(max_length=32)
    mobile = fields.CharField(max_length=32)
    province = fields.CharField(max_length=32, description="省")
    city = fields.CharField(max_length=32, description="市")
    district = fields.CharField(max_length=32, description="区")
    address = fields.CharField(max_length=255, description="详细地址")
    isDefault = fields.BooleanField(description="是否为默认地址", default=False)
    customer = fields.ForeignKeyField("models.Customer", related_name="addresses")


from enum import IntEnum


class CategoryType(IntEnum):
    first = 1
    second = 2
    third = 3


class Category(Model):
    """
    商品类别
    """
    name = fields.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = fields.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = fields.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    parent = fields.ForeignKeyField("models.Category", related_name="childs", null=True)
    category_type = fields.IntEnumField(CategoryType, null=True)
    imgUrl = fields.CharField(max_length=255, null=True)
    # 是否放荡首页展示表
    add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name


# class GoodsCategoryBrand(Model):
#     """
#     品牌名
#     """
#     category = fields.ForeignKeyField("models.GoodsCategory", null=True, verbose_name="商品类目",
#                                       related_name="brands")
#     name = fields.CharField(default="", max_length=30, verbose_name="品牌名", help_text="品牌名")
#     desc = fields.TextField(default="", max_length=200, verbose_name="品牌描述", help_text="品牌描述")
#     imgUrl = fields.CharField(max_length=255)  # 注意max_length
#     add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "品牌"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class Goods(Model):
    """
    商品
    """
    category = fields.ForeignKeyField("models.Category", verbose_name="商品类目")
    goods_sn = fields.CharField(max_length=50, default="", verbose_name="商品唯一货号")  # 商品编码
    name = fields.CharField(max_length=30, verbose_name="商品名")
    click_num = fields.IntField(default=0, verbose_name="点击数")  # 点击数
    sold_num = fields.IntField(default=0, verbose_name="卖出数")  # 卖出数
    fav_num = fields.IntField(default=0, verbose_name="收藏数")  #
    goods_num = fields.IntField(default=0, verbose_name="库存")  # 库存
    market_price = fields.FloatField(default=0, verbose_name="市场价格")
    shop_price = fields.FloatField(default=0, verbose_name="本店售价")  # 商店售价
    goods_brief = fields.TextField(max_length=500, verbose_name="商品简述")
    # goods_desc = MDTextField(verbose_name="商品详述")  # 富文本使用DjangoUeditor
    ship_free = fields.BooleanField(default=True, verbose_name="是否承担运费")  # 是否承担运费
    goods_front_image = fields.CharField(max_length=255, verbose_name="封面图片", )  # 封面图片
    goods_front_image_url = fields.CharField(max_length=300, default="", verbose_name="封面图片链接")
    is_new = fields.BooleanField(default=False, verbose_name="是否新品")  # 是否为新品
    is_hot = fields.BooleanField(default=False, verbose_name="是否热卖")  # 是否为热卖
    add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")


class GoodsImage(Model):
    """
    商品图
    """
    goods = fields.ForeignKeyField("models.Goods", related_name="images", verbose_name="商品")
    image_url = fields.CharField(max_length=255, verbose_name="图片链接")
    add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")


class Banner(Model):
    """
    轮播的商品
    """
    goods = fields.ForeignKeyField("models.Goods", verbose_name="商品")
    image = fields.CharField(max_length=255, verbose_name="轮播图片")
    index = fields.IntField(default=0, verbose_name="轮播顺序")
    add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")


class IndexAd(Model):
    category = fields.ForeignKeyField("models.Category", related_name='category',
                                      verbose_name="商品类目")
    goods = fields.ForeignKeyField("models.Goods", verbose_name="商品")


class HotSearchWords(Model):
    """
    热搜词
    """
    keywords = fields.CharField(default="", max_length=20, verbose_name="热搜词")
    index = fields.IntField(default=0, verbose_name="排序")
    add_time = fields.DatetimeField(auto_now_add=True, verbose_name="添加时间")
