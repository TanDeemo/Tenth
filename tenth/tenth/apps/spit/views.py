from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_redis import get_redis_connection

from spit.models import Spit
from spit.serializers import SpitSerializer


# Create your views here.
class SpitViewSet(ModelViewSet):
    """吐槽视图集"""
    queryset = Spit.objects.all()

    def perform_authentication(self, request):
        pass

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(parent=None).order_by('-publishtime')
        spit_list = []
        try:
            user = request.user
        except Exception:
            user = None

        if user and user.is_authenticated:
            for spit in queryset:
                redis_conn = get_redis_connection('spit')
                collected = redis_conn.hget(f'collected_{spit.id}', user.id)
                thumbup = redis_conn.hget(f'thumbup_{spit.id}', user.id)
                if collected:
                    spit.collected = True
                if thumbup:
                    spit.hasthumbup = True
                spit_list.append(spit)
        else:
            spit_list = queryset

        serializer = SpitSerializer(spit_list, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='collect')
    def collect_spit(self, request, *args, **kwargs):
        spit = self.get_object()
        try:
            user = request.user
        except Exception:
            user = None

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            collected = redis_conn.hget(f'collected_{spit.id}', user.id)
            if collected:
                redis_conn.hdel(f'collected_{spit.id}', user.id)
                return Response({'message': '取消收藏成功', 'success': True})
            else:
                redis_conn.hset(f'collected_{spit.id}', user.id, 1)
                return Response({'message': '收藏成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['put'], detail=True, url_path='updatethumbup')
    def updatethumbup_spit(self, request, *args, **kwargs):
        spit = self.get_object()
        try:
            user = request.user
        except Exception:
            user = None

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            thumbup = redis_conn.hget(f'thumbup_{spit.id}', user.id)
            if thumbup:
                redis_conn.hdel(f'thumbup_{spit.id}', user.id)
                spit.thumbup -= 1
                spit.save()
                return Response({'message': '取消点赞成功', 'success': True})
            else:
                redis_conn.hset(f'thumbup_{spit.id}', user.id, 1)
                spit.thumbup += 1
                spit.save()
                return Response({'message': '点赞成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        data = request.data
        parent_id = data.get('parent', '')
        if parent_id:
            spit = Spit.objects.get(pk=parent_id)
            try:
                user = request.user
                data['userid'] = user.id
                data['nickname'] = user.username
                data['avatar'] = user.avatar
                spit.comment += 1
                spit.save()
            except Exception:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = SpitSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        spit = self.get_object()
        spit.visits += 1
        spit.save()
        try:
            user = request.user
        except Exception:
            user = None
        if user and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            thumbup = redis_conn.hget(f'thumbup_{spit.id}', user.id)
            if thumbup:
                spit.hasthumbup = True
        serializer = SpitSerializer(spit)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='children')
    def children_spit(self, request, *args, **kwargs):
        try:
            user = request.user
        except Exception:
            user = None
        spit = self.get_object()
        queryset = []
        spit_set = self.get_queryset().filter(parent=spit).order_by('-publishtime')
        if user and user.is_authenticated:
            for spit_children in spit_set:
                redis_conn = get_redis_connection('spit')
                thumbup = redis_conn.hget(f'thumbup_{spit_children.id}', user.id)
                if thumbup:
                    spit_children.hasthumbup = True
                queryset.append(spit_children)
        else:
            queryset = spit_set
        serializer = SpitSerializer(queryset, many=True)
        return Response(serializer.data)




