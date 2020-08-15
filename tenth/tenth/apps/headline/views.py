from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from drf_haystack.viewsets import HaystackViewSet

from headline.serializers import ChannelSerializer, CreateArticleSerializer, ListArticleSerializer, \
    ArticleDetailSerializer, ArticleCommentSerializer, ArticleSearchSerializer
from headline.models import Channel, Article
from headline.search_indexes import ArticleIndex


# Create your views here.
class ChannelsViewSet(ReadOnlyModelViewSet):
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all().order_by('pk')


class ArticleViewSet(ModelViewSet):
    """文章视图集"""
    queryset = Article.objects.all()

    def create(self, request, *args, **kwargs):
        """新建文章"""
        user = self.request.user
        if user.is_authenticated:
            data = request.data
            data['user'] = user.id
            serializer = CreateArticleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response({'articleid': instance.id, 'success': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=True, url_path='channel')
    def get_channel_article(self, request, pk):
        """首页文章显示"""
        if pk == '-1':
            queryset = self.get_queryset()
        else:
            queryset = Article.objects.filter(channel_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListArticleSerializer(page, many=True, context={'user': request.user})
            return self.get_paginated_response(serializer.data)

        serializer = ListArticleSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='collect')
    def collect_article(self, request, pk):
        """收藏和取消收藏"""
        if request.user.is_authenticated:
            article = Article.objects.get(pk=pk)
            if request.user in article.collected_users.all():
                article.collected_users.remove(request.user)
                article.save()
                return Response({'message': '取消收藏成功', 'success': True}, status=status.HTTP_200_OK)
            else:
                article.collected_users.add(request.user)
                article.save()
                return Response({'message': '收藏成功', 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '收藏失败, 请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        article = Article.objects.get(pk=kwargs.get('pk'))
        article.visits += 1
        article.save()
        instance = self.get_object()
        serializer = ArticleDetailSerializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='publish_comment')
    def comment_article(self, request, pk):
        article = self.get_object()
        article.comment_count += 1
        article.save()
        user = request.user
        if user.is_authenticated:
            data = request.data
            data['user'] = user.id
            serializer = ArticleCommentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': '评论成功', 'success': True})
        else:
            return Response({'message': '评论失败, 请先登录', 'success': False})


class ArticleSearchView(HaystackViewSet):
    index_models = [Article]
    serializer_class = ArticleSearchSerializer

