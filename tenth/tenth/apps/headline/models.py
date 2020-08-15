from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from question.models import Label
from users.models import User


class Article(models.Model):
    title = models.CharField(max_length=100, null=True, default=None, verbose_name="标题")
    content = RichTextUploadingField(default='', verbose_name='文章内容')
    image = models.CharField(max_length=100, default=None, verbose_name="文章封面")
    createtime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建日期")
    updatetime = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")
    visits = models.IntegerField(null=True, default=0, verbose_name="浏览量")
    thumbup = models.IntegerField(null=True, default=0, verbose_name="点赞数")
    comment_count = models.IntegerField(null=True, default=0, verbose_name="评论数")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='用户ID')
    channel = models.ForeignKey("Channel", related_name="articles", on_delete=models.CASCADE, null=True, default=None,
                                verbose_name="所属频道")
    labels = models.ManyToManyField(Label, symmetrical=False, related_name='articles')  # 这个问题属于哪些标签的
    collected_users = models.ManyToManyField(User, symmetrical=False, related_name='collected_articles')  # 被哪些用户收藏

    class Meta:
        db_table = "tb_article"
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-createtime']

    def __str__(self):
        return self.title


class Channel(models.Model):
    name = models.CharField(max_length=100, null=True, default=None, verbose_name="频道名称")

    class Meta:
        db_table = "tb_channel"
        verbose_name = "频道"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.CharField(max_length=1000, default='', verbose_name='回答内容')
    createtime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建日期")
    updatetime = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='父评论')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments", default=None,
                                verbose_name="问题ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", default=None, verbose_name="用户ID")

    class Meta:
        db_table = "article_comment"
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-createtime']  # 指明默认排序

    def __str__(self):
        return self.content
