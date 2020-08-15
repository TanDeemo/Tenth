from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django_redis import get_redis_connection
from users.serializers import RegisterSerializer, LoginSerializer, UserInfoSerializer
from users.models import User
from question.models import Label
from random import randint
import datetime
import re
import logging
logger = logging.getLogger('django')


# Create your views here.
class SendSMSView(APIView):
    """发送短信"""

    def get(self, request, mobile):
        redis_conn = get_redis_connection('verify_code')
        flag = redis_conn.get(f'flag_{mobile}')
        if flag:
            return Response({'success': False,
                             'message': '发送失败,请稍等3分钟后再试'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return Response({'success': False,
                             'message': '手机号码格式不正确'},
                            status=status.HTTP_400_BAD_REQUEST)

        count = User.objects.filter(mobile=mobile).count()
        if count:
            return Response({'success': False,
                             'message': '手机号已注册'},
                            status=status.HTTP_400_BAD_REQUEST)

        sms_code = f'{randint(0, 999999):06d}'
        logger.info(sms_code)

        pipe = redis_conn.pipeline()
        pipe.setex(f'sms_{mobile}', 180, sms_code)
        pipe.setex(f'flag_{mobile}', 180, 1)
        pipe.execute()

        return Response({'success': True,
                         'message': '发送成功',
                         'sms_code': sms_code})


class RegisterView(CreateAPIView):
    """注册用户视图"""
    serializer_class = RegisterSerializer
    queryset = User.objects.all().order_by('pk')


class LoginView(CreateAPIView):
    """登陆视图"""
    serializer_class = LoginSerializer
    queryset = User.objects.all().order_by('pk')


class UserInfoView(RetrieveUpdateAPIView):
    """用户详情"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer
    queryset = User.objects.all().order_by('pk')


    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        birthday = request.data.get('birthday', '')
        if birthday:
            try:
                if '.' in birthday:
                    birthday = datetime.datetime.strptime(birthday, '%Y.%m.%d').date()
                elif '/' in birthday:
                    birthday = datetime.datetime.strptime(birthday, '%Y/%m/%d').date()
                elif ' ' in birthday:
                    birthday = datetime.datetime.strptime(birthday, '%Y %m %d').date()
            except Exception:
                raise APIException('日期不正确')
        request.data['birthday'] = birthday
        return super(UserInfoView, self).put(request, *args, **kwargs)


class UserLabelView(APIView):

    def put(self, request):
        user = request.user
        labels_id = request.data.get('labels')
        if user.is_authenticated:
            user.labels.clear()
            for i in labels_id:
                user.labels.add(i)
            return Response({})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserLikeView(APIView):

    def post(self, request, pk):
        user = request.user
        user.idols.add(pk)
        return Response({'message': '关注成功', 'success': True})

    def delete(self, request, pk):
        user = request.user
        user.idols.remove(pk)
        return Response({'message': '取消关注成功', 'success': True})