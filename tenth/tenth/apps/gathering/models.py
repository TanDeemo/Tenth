from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
from users.models import User


class Gathering(models.Model):
    STATE_CHOICES = (
        (0, "不可见"),
        (1, "可见"),
    )
    name = models.CharField(max_length=100, null=True,default=None, verbose_name="活动名称")
    summary = models.TextField(null=True,default=None, verbose_name="活动简介")
    detail = RichTextUploadingField(default='', verbose_name='详细介绍')
    address = models.CharField(max_length=100, null=True, default=None, verbose_name="举办地点")
    sponsor = models.CharField(max_length=100, null=True, default=None, verbose_name="主办方")
    image = models.ImageField(null=True, default=None, verbose_name="活动图片")
    city = models.CharField(max_length=100, null=True, default=None, verbose_name="举办城市")
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=1, verbose_name="是否可见")
    starttime = models.DateTimeField(null=True,verbose_name="开始时间")
    endtime = models.DateTimeField(null=True,verbose_name="截止日期")
    endrolltime = models.DateTimeField(null=True, verbose_name="报名截止日期")
    users = models.ManyToManyField(User, symmetrical=False, related_name='gathers', verbose_name="参加者")

    class Meta:
        db_table = "tb_gathering"
        verbose_name = "活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

