from drf_haystack.serializers import HaystackSerializer
from rest_framework import serializers

from headline.models import Channel, Article, Comment
from headline.search_indexes import ArticleIndex
from users.models import User


# from django.contrib.auth import get_user_model
# User = get_user_model()


class ChannelSerializer(serializers.ModelSerializer):
    """频道组序列化器"""

    class Meta:
        model = Channel
        fields = '__all__'


class CreateArticleSerializer(serializers.ModelSerializer):
    """创建文章序列化器"""
    image = serializers.CharField(allow_blank=True, default=None, required=False)

    class Meta:
        model = Article
        fields = ('title', 'content', 'image', 'labels', 'channel', 'user')


class AuthorArticleSerializer(serializers.ModelSerializer):
    """作者文章序列化"""

    class Meta:
        model = Article
        fields = ('id', 'title')


class AuthorSerializer(serializers.ModelSerializer):
    """作者序列化器"""
    articles = AuthorArticleSerializer(label='作者所有文章', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'articles', 'fans')


class ListArticleSerializer(serializers.ModelSerializer):
    """首页文章序列化器"""
    user = AuthorSerializer(label='作者序列化器', read_only=True)
    collected = serializers.SerializerMethodField(label='当前用户是否收藏此文章')

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'createtime', 'user', 'collected_users', 'collected', 'image')

    def get_collected(self, instance):
        user = self.context['user']
        if user.is_authenticated:
            collected_articles_list = user.collected_articles.all()
            return True if instance in collected_articles_list else False
        else:
            return False


class SubsSerializer(serializers.ModelSerializer):
    """评论嵌套序列化"""

    user = AuthorSerializer(label='作者序列化器', read_only=True)
    subs = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'article', 'user', 'parent', 'subs', 'createtime')


class CommentsSerializer(serializers.ModelSerializer):
    """文章评论序列化器"""

    user = AuthorSerializer(label='作者序列化器', read_only=True)
    subs = SubsSerializer(label='评论的评论', many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    user = AuthorSerializer(label='作者序列化器', read_only=True)
    comments = CommentsSerializer(label='文章评论', read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'


class ArticleCommentSerializer(serializers.ModelSerializer):
    """文章评论保存序列化器"""

    class Meta:
        model = Comment
        fields = ('id', 'article', 'content', 'parent', 'user')


class ArticleSearchSerializer(HaystackSerializer):
    """文章搜索序列化器"""

    class Meta:
        index_classes = [ArticleIndex]
        fields = ('text', 'id', 'title', 'content', 'createtime')
