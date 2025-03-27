from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers

# Create your models here.

# 用户表
class User(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    username = models.CharField(max_length=255, db_index=True, verbose_name="用户名",help_text="用户名")
    password = models.CharField(max_length=255, null=True, blank=True,verbose_name="密码", help_text="密码")
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="昵称", help_text="昵称")
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    address = models.CharField(max_length=255, verbose_name="地址", null=True, blank=True, help_text="地址")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    uid = models.CharField(max_length=100, verbose_name="用户唯一id", null=True, blank=True, help_text="用户唯一id")
    role = models.CharField(max_length=255, verbose_name="角色", null=True, blank=True, help_text="角色")
    deleted = models.IntegerField(verbose_name="逻辑删除", null=True, blank=True, help_text="逻辑删除",default=0)
    score = models.IntegerField(verbose_name="积分", null=True, blank=True, help_text="积分",default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",verbose_name="修改时间")

    class Meta:
        db_table = "sys_user"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# 权限菜单
class Permission(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, null=True, verbose_name="权限名称", help_text="权限名称")
    path = models.CharField(max_length=255, null=True, verbose_name="路径", help_text="路径")
    orders = models.IntegerField(verbose_name="顺序", null=True, blank=True, help_text="顺序")
    icon = models.CharField(max_length=255, null=True, verbose_name="图标", help_text="图标")
    page = models.CharField(max_length=255, null=True, verbose_name="页面路径", help_text="页面路径")
    auth = models.CharField(max_length=255, null=True, verbose_name="权限", help_text="权限")
    p_id = models.IntegerField(verbose_name="父ID", null=True, blank=True, help_text="父ID")
    deleted = models.IntegerField(verbose_name="逻辑删除", null=True, blank=True, help_text="逻辑删除",default=0)
    type = models.IntegerField(verbose_name="类型", null=True, blank=True, help_text="类型")
    hide = models.BooleanField(verbose_name="是否隐藏", null=True, blank=True, help_text="是否隐藏")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",verbose_name="修改时间")

    class Meta:
        db_table = "sys_permission"
        verbose_name = "权限菜单表"
        verbose_name_plural = verbose_name

class PermissionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = '__all__'


# 角色表
class Role(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, verbose_name="角色名称", help_text="角色名称")
    flag = models.CharField(max_length=255, verbose_name="唯一标识", help_text="唯一标识")
    deleted = models.IntegerField(verbose_name="逻辑删除", null=True, blank=True, help_text="逻辑删除",default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="修改时间",verbose_name="修改时间")
    permission = models.ManyToManyField(Permission)

    class Meta:
        db_table = "sys_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name

class RoleSerializer(serializers.ModelSerializer):
    permissionIds = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    def get_permissionIds(self, obj):
        return [permission.id for permission in obj.permission.all()]


# 数据字典
class SysDict(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    code = models.CharField(max_length=255, verbose_name="编码", help_text="编码")
    value = models.CharField(max_length=255, null=True, verbose_name="内容", help_text="内容")
    type = models.CharField(max_length=10, null=True, verbose_name="类型", help_text="类型")
    deleted = models.IntegerField(verbose_name="逻辑删除", null=True, blank=True, help_text="逻辑删除", default=0)

    class Meta:
        db_table = "dict"
        verbose_name = "数据字典表"
        verbose_name_plural = verbose_name

class SysDictSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysDict
        fields = '__all__'


# 网站公告
class Notice(models.Model):
    id = models.AutoField(primary_key=True, help_text="Id", verbose_name="Id")
    name = models.CharField(max_length=255, verbose_name="标题 ", null=True, blank=True, help_text="标题")
    content = models.TextField(verbose_name="内容 ",null=True, blank=True,  help_text="内容")
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间", verbose_name="创建时间")
    user_id = models.IntegerField(verbose_name="发布者", null=True, blank=True, help_text="发布者")

    @property
    def userId(self):
        return self.user_id
    @property
    def createTime(self):
        return self.create_time
		
    class Meta:
        db_table = "notice"
        verbose_name = "网站公告"
        verbose_name_plural = verbose_name

class NoticeSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    createTime = serializers.SerializerMethodField()
	
    class Meta:
        model = Notice
        fields = '__all__'

    def get_userId(self, obj):
        return obj.user_id
    def get_createTime(self, obj):
        return obj.create_time		
