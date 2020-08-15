from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from gathering.models import Gathering
from gathering.serializers import GatheringSerializer


# Create your views here.
class GatheringViewSet(ModelViewSet):
    """活动视图集"""
    queryset = Gathering.objects.filter(state=1).order_by('-starttime')
    serializer_class = GatheringSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='join')
    def join_gathering(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            instance = self.get_object()
            if user in instance.users.all():
                instance.users.remove(user)
                instance.save()
                return Response({'message': '取消报名成功', 'success': True})
            else:
                instance.users.add(user)
                instance.save()
                return Response({'message': '报名成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)



