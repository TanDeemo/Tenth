from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from django.db import DataError


def exception_handler(exc, context):
    """自定义异常处理函数"""
    response = drf_exception_handler(exc, context)
    if response is None:
        if isinstance(exc, DataError):
            response = Response({'errmsg': '数据库出错'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


