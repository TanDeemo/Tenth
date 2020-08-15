from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from users.models import User


class Enterprise(models.Model):
    name = models.CharField(max_length=100, null=True,default=None, verbose_name="企业名称")
    summary = models.CharField(max_length=1000, null=True,default=None, verbose_name="企业简介")
    content = models.CharField(max_length=1000, null=True, default=None, verbose_name="企业详细信息")
    city = models.CharField(max_length=100, null=True, default=None, verbose_name="企业所在城市")
    address = models.CharField(max_length=100, null=True,default=None, verbose_name="企业地址")
    labels = models.CharField(max_length=100, null=True,default=None, verbose_name="标签列表", help_text="多个标签以空格隔开")
    coordinate = models.CharField(max_length=100, null=True,default=None, verbose_name="企业坐标")
    logo = models.ImageField(null=True,default=None, verbose_name="Logo")
    url = models.CharField(max_length=100, null=True,default=None, verbose_name="URL")
    visits = models.BigIntegerField(null=True, default=0, verbose_name="浏览量")
    users = models.ManyToManyField(User, symmetrical=False, related_name='enterpises', verbose_name="收藏者")

    class Meta:
        db_table = "tb_enterprise"
        verbose_name = "企业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Recruit(models.Model):
    STATE_CHOICES = (
        (0, "不可用"),
        (1, "可用"),
    )
    jobname = models.CharField(max_length=100, null=True, default=None, verbose_name="职位名称")
    salary = models.CharField(max_length=1000, null=True, default=None, verbose_name="薪资范围")
    condition = models.CharField(max_length=100, null=True, default=None, verbose_name="经验要求")
    education = models.CharField(max_length=100, null=True, default=None, verbose_name="学历要求")
    type = models.CharField(max_length=10, null=True, default=None, verbose_name="任职方式")
    city = models.CharField(max_length=100, null=True, default=None, verbose_name="办公所在城市")
    address = models.CharField(max_length=100, null=True, default=None, verbose_name="办公地址")
    state = models.SmallIntegerField(choices=STATE_CHOICES, null=True, default=1, verbose_name="状态")
    labels = models.CharField(max_length=100, null=True, default=None, verbose_name="职位标签", help_text="多个标签以空格隔开")
    detailcontent = RichTextUploadingField(default='', verbose_name='职位描述')
    detailrequire = RichTextUploadingField(default='', verbose_name='职位要求')
    visits = models.BigIntegerField(null=True, default=0, verbose_name="浏览量")
    createtime = models.DateTimeField(null=True, auto_now_add=True, verbose_name="创建日期")
    enterprise = models.ForeignKey(Enterprise, related_name="recruits", on_delete=models.CASCADE, null=True, default=None, verbose_name="企业ID")
    users = models.ManyToManyField(User, symmetrical=False, related_name='retruits', verbose_name="收藏者")

    class Meta:
        db_table = "tb_recruit"
        verbose_name = "职位"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.enterprise.name + "_" + self.jobname


class City(models.Model):
    HOT_CHOICES = (
        (0, "不是热门"),
        (1, "是热门"),
    )
    name = models.CharField(max_length=20, null=True,default=None, verbose_name="城市名称")
    ishot = models.SmallIntegerField(choices=HOT_CHOICES, null=True, default=1, verbose_name="是否热门")

    class Meta:
        db_table = "tb_city"
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
