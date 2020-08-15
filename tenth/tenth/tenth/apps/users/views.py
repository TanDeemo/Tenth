from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from users.serializers import RegisterSerializer, LoginSerializer
from users.models import User
from random import randint
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