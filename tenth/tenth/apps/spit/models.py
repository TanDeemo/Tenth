import mongoengine

from django.utils import timezone


# 吐槽和吐槽的评论数据都存储在mongodb中,不是存储在mysql中
# 吐槽和吐槽的评论都属于吐槽的这张表
# 吐槽的parent_id为None,评论则有parent_id
class Spit(mongoengine.Document):
    content = mongoengine.StringField()  # 吐槽内容
    publishtime = mongoengine.DateTimeField(default=timezone.now)  # 发布日期
    userid = mongoengine.StringField()  # 发布人ID
    nickname = mongoengine.StringField()  # 发布人昵称
    visits = mongoengine.IntField(default=0)  # 浏览量
    thumbup = mongoengine.IntField(default=0)  # 点赞数
    comment = mongoengine.IntField(default=0)  # 回复数
    avatar = mongoengine.StringField()  # 用户的头像
    parent = mongoengine.ReferenceField("Spit")  # 上级ID
    collected = mongoengine.BooleanField(default=False)  # 是否收藏
    hasthumbup = mongoengine.BooleanField(default=False)  # 是否点赞

    meta = {'collection': 'spit'}

    def __unicode__(self):
        return self.content
