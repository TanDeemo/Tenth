from rest_framework import serializers

from question.models import Label, Question, Reply
from headline.models import Article
from users.models import User


class UserQuestionSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class LabelSerializer(serializers.ModelSerializer):
    """标签序列化器"""
    class Meta:
        model = Label
        fields = ('id', 'label_name')


class GETQuestionByLabelsSerializer(serializers.ModelSerializer):
    """最新问答序列化器"""

    labels = serializers.StringRelatedField(label='问题绑定标签', read_only=True, many=True)

    class Meta:
        model = Question
        fields = ('id', 'createtime', 'labels', 'reply', 'replyname', 'replytime', 'title', 'unuseful_count',
                  'useful_count', 'user', 'visits')


class CreateQuestionsSerializer(serializers.ModelSerializer):
    """创建问题序列化器"""

    class Meta:
        model = Question
        fields = ('content', 'labels', 'title' , 'user')


class SubsCommentQuestionSerializer(serializers.ModelSerializer):
    """问题回答评论嵌套序列化器"""
    subs = serializers.StringRelatedField(label='嵌套评论')
    user = UserQuestionSerializer(label='用户', read_only=True)
    parent = serializers.SerializerMethodField(label='父类评论')

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', 'useful_count', 'problem', 'unuseful_count', 'subs', 'user', 'parent')

    def get_parent(self, instance):
        return None


class CommentQuestionDetailSerializer(serializers.ModelSerializer):
    """问题评论序列化器"""

    subs = SubsCommentQuestionSerializer(read_only=True, many=True)
    user = UserQuestionSerializer(label='用户', read_only=True)
    parent = serializers.SerializerMethodField(label='父类评论')

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', 'useful_count', 'problem', 'unuseful_count', 'subs', 'user', 'parent')

    def get_parent(self, instance):
        return None


class QuestionDetailSerializer(serializers.ModelSerializer):
    """问题详情序列化器"""

    labels = serializers.StringRelatedField(label='问题绑定标签', read_only=True, many=True)
    comment_question = serializers.SerializerMethodField(label='问题评论')
    answer_question = serializers.SerializerMethodField(label='问题回答')
    user = serializers.StringRelatedField(label='用户名', read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'createtime', 'labels', 'reply', 'replyname', 'replytime', 'title', 'unuseful_count',
                  'useful_count', 'user', 'visits', 'content', 'comment_question', 'answer_question', )

    def get_comment_question(self, instance):
        comment_questions = instance.replies.all().exclude(type__in=[1, 2])
        serializer = None
        if comment_questions:
            serializer = CommentQuestionDetailSerializer(comment_questions, many=True)
        return serializer.data if serializer else []


    def get_answer_question(self, instance):
        answer_questions = instance.replies.all().exclude(type__in=[0, 1])
        serializer = None
        if answer_questions:
            serializer = CommentQuestionDetailSerializer(answer_questions, many=True)
        return serializer.data if serializer else []


class ReplySerializerForCreate(serializers.ModelSerializer):
    """创建回答序列化器"""
    class Meta:
        model = Reply
        fields = ('problem', 'content', 'type', 'parent', 'user')


class LabelQuestionSerializer(serializers.ModelSerializer):
    """关联标签问答序列化器"""
    labels = serializers.StringRelatedField(read_only=True, many=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'createtime', 'labels', 'replyname', 'replytime', 'title', 'unuseful_count', 'useful_count',
                  'user', 'visits')


class LabelArticlesSerializer(serializers.ModelSerializer):
    """关联标签文章序列化器"""
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'


class LabelDetailSerializer(serializers.ModelSerializer):
    """标签详情序列化器"""

    questions = serializers.SerializerMethodField(label='关联标签的问答')
    articles = serializers.SerializerMethodField(label='标签关联的文章')


    class Meta:
        model = Label
        fields = ('id', 'questions', 'articles',  'label_name', 'desc', 'baike_url', 'label_icon', 'users')

    def get_questions(self, instance):
        questions = instance.questions.all()
        serializer = None
        if questions:
            serializer = LabelQuestionSerializer(questions, many=True)
        return serializer.data if serializer else []

    def get_articles(self, instance):
        articles = instance.articles.all()
        serializer = None
        if articles:
            serializer = LabelArticlesSerializer(articles, many=True)
        return serializer.data if serializer else []


class LabelsAllSerializer(serializers.ModelSerializer):
    """标签full序列化器"""
    class Meta:
        model = Label
        fields = '__all__'