from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.
from users.models import User


class Label(models.Model):

    label_name = models.CharField(max_length=20, null=True, default=None, verbose_name="标签名称")
    desc = models.CharField(max_length=200, null=True, default=None, verbose_name="标签描述")
    baike_url = models.CharField(max_length=200, null=True, default=None, verbose_name="标签百科链接")
    label_icon = models.ImageField(null=True, default=None, verbose_name="标签图片")
    # 标签的关注者
    users = models.ManyToManyField(User, symmetrical=False, related_name='labels', verbose_name="关注者")

    class Meta:
        db_table = "tb_label"
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.label_name


class Question(models.Model):
    title = models.CharField(max_length=100, null=True,default=None, verbose_name="标题")
    content = RichTextUploadingField(default='', verbose_name='问题内容')
    visits = models.BigIntegerField(null=True,default=0, verbose_name="浏览量")
    thumbup = models.BigIntegerField(null=True,default=0, verbose_name="点赞数")
    reply = models.BigIntegerField(null=True, default=0, verbose_name="回复数")
    useful_count = models.BigIntegerField(null=True, default=0, verbose_name="有用数")
    unuseful_count = models.BigIntegerField(null=True, default=0, verbose_name="无用数")
    solve = models.CharField(max_length=1, null=True, default=None, verbose_name="是否解决")
    createtime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建日期")
    updatetime = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")
    replyname = models.CharField(max_length=100, null=True,default=None, verbose_name="回复人昵称")
    replytime = models.DateTimeField(null=True,default=None, verbose_name="回复日期")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions", default=None, verbose_name="用户ID")
    labels = models.ManyToManyField(Label, symmetrical=False, related_name='questions')  # 这个问题属于哪些标签的

    class Meta:
        db_table = "tb_question"
        verbose_name = "问题"
        verbose_name_plural = verbose_name
        ordering = ['-createtime']

    def __str__(self):
        return self.title

class Reply(models.Model):

    content = RichTextUploadingField(default='', verbose_name='回答内容')
    createtime = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建日期")
    updatetime = models.DateTimeField(auto_now=True, null=True, verbose_name="修改日期")
    useful_count = models.BigIntegerField(null=True,default=0, verbose_name="有用数")
    unuseful_count = models.BigIntegerField(null=True,default=0, verbose_name="无用数")
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,verbose_name='父评论')
    problem = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="replies", default=None,verbose_name="问题ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies", default=None, verbose_name="用户ID")
    type = models.IntegerField(default=0, verbose_name='回答类型') # 0:评论问题 1:评论回答 2:回答

    class Meta:
        db_table = "qa_reply"
        verbose_name = "回答"
        verbose_name_plural = verbose_name
        ordering = ['-createtime']  # 指明默认排序

    def __str__(self):
        return self.content
