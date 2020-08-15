from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from recruit.models import City, Enterprise, Recruit
from recruit.serializers import HotCitySerializer, RecruitSerializer, EnterpriseSerializer, EnterpriseDetailSerializer, \
    RecruitDetailSerializer


# Create your views here.
class HotCityViewSet(ReadOnlyModelViewSet):
    serializer_class = HotCitySerializer
    queryset = City.objects.filter(ishot=1).order_by('pk')
    pagination_class = None


class EnterpriseViewSet(ModelViewSet):
    queryset = Enterprise.objects.all()

    @action(methods=['put'], detail=True, url_path='visit')
    def enterprise_visit(self, request, *args, **kwargs):
        enterprise = self.get_object()
        enterprise.visits += 1
        enterprise.save()
        return Response({'message': '更新成功', 'success': True})

    @action(methods=['get'], detail=False, url_path='search/hotlist')
    def enterprise_hot(self, request):
        queryset = self.get_queryset().order_by('-visits')
        serializer = EnterpriseSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='collect')
    def collect_enterprise(self, request, *args, **kwargs):
        enterprise = self.get_object()
        user = request.user
        if user.is_authenticated:
            enterprises = user.enterpises.all()
            if enterprise in enterprises:
                return Response({'message': '已收藏请勿重复点击', 'success': False})
            else:
                user.enterpises.add(enterprise)
                return Response({'message': '收藏成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=True, url_path='cancelcollect')
    def cancelcollect_enterprise(self, request, *args, **kwargs):
        enterprise = self.get_object()
        user = request.user
        if user.is_authenticated:
            enterprises = user.enterpises.all()
            if enterprise in enterprises:
                user.enterpises.remove(enterprise)
                return Response({'message': '取消收藏成功', 'success': True})
            else:
                return Response({'message': '未收藏, 请勿重复点击', 'success': False})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        enterprise = self.get_object()
        serializer = EnterpriseDetailSerializer(enterprise)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)


class RecruitsViewSet(ModelViewSet):
    queryset = Recruit.objects.all()

    @action(methods=['get'], detail=False, url_path='search/recommend')
    def recommend_recruit(self, request):
        queryset = self.get_queryset().order_by('-visits')
        serializer = RecruitSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='search/latest')
    def last_recruit(self, request):
        queryset = self.get_queryset().order_by('-createtime')
        serializer = RecruitSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        recruit = self.get_object()
        serializer = RecruitDetailSerializer(recruit)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='visit')
    def recruits_visit(self, request, *args, **kwargs):
        recruit = self.get_object()
        recruit.visits += 1
        recruit.save()
        return Response({'message': '更新成功', 'success': True})

    @action(methods=['post'], detail=True, url_path='collect')
    def collect_recruits(self, request, *args, **kwargs):
        recruit = self.get_object()
        user = request.user
        if user.is_authenticated:
            recruits = user.retruits.all()
            if recruit in recruits:
                return Response({'message': '已收藏, 请勿重复点击', 'success': False})
            else:
                user.retruits.add(recruit)
                return Response({'message': '收藏成功', 'success': True})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=True, url_path='cancelcollect')
    def cancelcollect_recruits(self, request, *args, **kwargs):
        recruit = self.get_object()
        user = request.user
        if user.is_authenticated:
            recruits = user.retruits.all()
            if recruit in recruits:
                user.retruits.remove(recruit)
                return Response({'message': '取消收藏成功', 'success': True})
            else:
                return Response({'message': '未收藏, 请勿重复点击', 'success': False})
        else:
            return Response({'message': '请先登录', 'success': False}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=False, url_path='search/city/keyword')
    def search_recruit(self, request, *args, **kwargs):
        city = request.data.get('cityname')
        keyword = request.data.get('keyword')
        if city and keyword:
            queryset = Recruit.objects.filter(city=city, jobname__contains=keyword)
        elif city:
            queryset = Recruit.objects.filter(city=city)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = RecruitSerializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)



