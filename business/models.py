from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers


# Create your models here.
# 用户
class Member(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    username = models.CharField(max_length=255, verbose_name="用户名 ", null=True, blank=True, help_text="用户名")
    name = models.CharField(max_length=255, verbose_name="姓名 ", null=True, blank=True, help_text="姓名")
    user_id = models.IntegerField(verbose_name="所属用户", null=True, blank=True, help_text="所属用户")

    @property
    def userId(self):
        return self.user_id

    class Meta:
        db_table = "member"
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class MemberSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id


# 股票市场类型
class Category(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="类型名称 ", null=True, blank=True, help_text="类型名称")

    class Meta:
        db_table = "category"
        verbose_name = "股票市场类型"
        verbose_name_plural = verbose_name


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# 股票数据
class Stock(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="股票名称 ", null=True, blank=True, help_text="股票名称")
    content = models.TextField(verbose_name="公司简介 ", null=True, blank=True, help_text="公司简介")
    code = models.CharField(max_length=255, verbose_name="股票代码 ", null=True, blank=True, help_text="股票代码")
    category_id = models.IntegerField(verbose_name="股票市场类型", null=True, blank=True, help_text="股票市场类型")
    industry_id = models.IntegerField(verbose_name="板块行业", null=True, blank=True, help_text="板块行业")
    province = models.CharField(max_length=255, verbose_name="省份 ", null=True, blank=True, help_text="省份")
    address = models.CharField(max_length=255, verbose_name="公司地址 ", null=True, blank=True, help_text="公司地址")
    company = models.CharField(max_length=255, verbose_name="公司名称 ", null=True, blank=True, help_text="公司名称")
    views = models.IntegerField(verbose_name="浏览量", null=True, blank=True, help_text="浏览量")

    @property
    def categoryId(self):
        return self.category_id

    @property
    def industryId(self):
        return self.industry_id

    class Meta:
        db_table = "stock"
        verbose_name = "股票数据"
        verbose_name_plural = verbose_name


class StockSerializer(serializers.ModelSerializer):
    categoryId = serializers.SerializerMethodField()
    industryId = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = '__all__'

    def get_categoryId(self, obj):
        return obj.category_id

    def get_industryId(self, obj):
        return obj.industry_id


# 板块行业
class Industry(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    name = models.CharField(max_length=255, verbose_name="板块名称 ", null=True, blank=True, help_text="板块名称")

    class Meta:
        db_table = "industry"
        verbose_name = "板块行业"
        verbose_name_plural = verbose_name


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'


# 股票收藏
class Collect(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    user_id = models.IntegerField(verbose_name="用户", null=True, blank=True, help_text="用户")
    stock_id = models.IntegerField(verbose_name="股票", null=True, blank=True, help_text="股票")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                       verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="更新时间",
                                       verbose_name="更新时间")

    @property
    def userId(self):
        return self.user_id

    @property
    def stockId(self):
        return self.stock_id

    @property
    def createTime(self):
        return self.create_time

    @property
    def updateTime(self):
        return self.update_time

    class Meta:
        db_table = "collect"
        verbose_name = "股票收藏"
        verbose_name_plural = verbose_name


class CollectSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    stockId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id

    def get_stockId(self, obj):
        return obj.stock_id

    def get_createTime(self, obj):
        return obj.create_time

    def get_updateTime(self, obj):
        return obj.update_time


# 用户标签
class Membertags(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    user_id = models.IntegerField(verbose_name="用户编号", null=True, blank=True, help_text="用户编号")
    industry_id = models.IntegerField(verbose_name="板块行业", null=True, blank=True, help_text="板块行业")

    @property
    def userId(self):
        return self.user_id

    @property
    def industryId(self):
        return self.industry_id

    class Meta:
        db_table = "membertags"
        verbose_name = "用户标签"
        verbose_name_plural = verbose_name


class MembertagsSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    industryId = serializers.SerializerMethodField()

    class Meta:
        model = Membertags
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id

    def get_industryId(self, obj):
        return obj.industry_id


# 股票评论
class Comments(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="评论编号", help_text="评论编号")
    content = models.TextField(verbose_name="评论内容 ", null=True, blank=True, help_text="评论内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="添加时间",
                                       verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",
                                       verbose_name="修改时间")
    user_id = models.IntegerField(verbose_name="用户", null=True, blank=True, help_text="用户")
    stock_id = models.IntegerField(verbose_name="课程编号", null=True, blank=True, help_text="课程编号")
    pid = models.IntegerField(verbose_name="父评论ID", null=True, blank=True, help_text="父评论ID")
    puser_id = models.IntegerField(verbose_name="父级用户ID", null=True, blank=True, help_text="父级用户ID")
    score = models.IntegerField(verbose_name="评论星级", null=True, blank=True, help_text="评论星级")

    @property
    def createTime(self):
        return self.create_time

    @property
    def updateTime(self):
        return self.update_time

    @property
    def userId(self):
        return self.user_id

    @property
    def stockId(self):
        return self.stock_id

    @property
    def puserId(self):
        return self.puser_id

    class Meta:
        db_table = "comments"
        verbose_name = "股票评论"
        verbose_name_plural = verbose_name


class CommentsSerializer(serializers.ModelSerializer):
    createTime = serializers.SerializerMethodField()
    updateTime = serializers.SerializerMethodField()
    userId = serializers.SerializerMethodField()
    stockId = serializers.SerializerMethodField()
    puserId = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_createTime(self, obj):
        return obj.create_time

    def get_updateTime(self, obj):
        return obj.update_time

    def get_userId(self, obj):
        return obj.user_id

    def get_stockId(self, obj):
        return obj.stock_id

    def get_puserId(self, obj):
        return obj.puser_id


# 股票价格数据
class Stockdata(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号", help_text="编号")
    code = models.CharField(max_length=255, verbose_name="股票代码 ", null=True, blank=True, help_text="股票代码")
    time = models.CharField(max_length=255, verbose_name="时间 ", null=True, blank=True, help_text="时间")
    newprice = models.FloatField(verbose_name="最新价 ", null=True, blank=True, help_text="最新价")
    openprice = models.FloatField(verbose_name="开盘价 ", null=True, blank=True, help_text="开盘价")
    lowprice = models.FloatField(verbose_name="最低价 ", null=True, blank=True, help_text="最低价")
    highprice = models.FloatField(verbose_name="最高价 ", null=True, blank=True, help_text="最高价")
    turnover = models.FloatField(verbose_name="成交量(手) ", null=True, blank=True, help_text="成交量(手)")
    amount = models.FloatField(verbose_name="成交额(元) ", null=True, blank=True, help_text="成交额(元)")
    chg = models.CharField(max_length=200, verbose_name="涨跌幅", null=True, blank=True, help_text="涨跌幅")

    class Meta:
        db_table = "stockdata"
        verbose_name = "股票价格数据"
        verbose_name_plural = verbose_name


class StockdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stockdata
        fields = '__all__'


# 轮播图
class Banner(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="轮播图编号", help_text="轮播图编号")
    img = models.CharField(max_length=255, verbose_name="图片 ", null=True, blank=True, help_text="图片")
    url = models.CharField(max_length=255, verbose_name="链接地址 ", null=True, blank=True, help_text="链接地址")
    index_radio = models.CharField(max_length=255, verbose_name="是否首页 ", null=True, blank=True,
                                   help_text="是否首页")

    @property
    def indexRadio(self):
        return self.index_radio

    class Meta:
        db_table = "banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name


class BannerSerializer(serializers.ModelSerializer):
    indexRadio = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = '__all__'

    def get_indexRadio(self, obj):
        return obj.index_radio
