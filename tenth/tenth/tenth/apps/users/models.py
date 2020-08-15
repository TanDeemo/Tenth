from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    SEX_CHOICES = (
        (1, "男"),
        (2, "女"),
    )
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', null=True)
    nickname = models.CharField(max_length=100, null=True, verbose_name='昵称')
    realname = models.CharField(max_length=100, null=True, verbose_name='真实名称')
    avatar = models.CharField(null=True, max_length=500, verbose_name="用户头像")
    sex = models.SmallIntegerField(choices=SEX_CHOICES, default=1, verbose_name="性别")
    birthday = models.DateField(null=True, verbose_name="出生年月日")
    website = models.CharField(max_length=100, null=True, verbose_name='个人网站')
    city = models.CharField(max_length=100, null=True, verbose_name='现居城市')
    address = models.CharField(max_length=100, null=True, verbose_name='联系住址')
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    fans = models.ManyToManyField(to='self', symmetrical=False, related_name='idols')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class OAuthWeixinUser(models.Model):
    """
    QQ登录用户数据
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_weixin'
        verbose_name = '微信登录用户数据'
        verbose_name_plural = verbose_name