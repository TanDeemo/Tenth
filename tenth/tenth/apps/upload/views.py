from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import APIException
from fdfs_client.client import Fdfs_client


# Create your views here.
class UploadImageViewSet(ViewSet):

    def upload_avatar(self, request):
        """上传头像"""
        avatar_url = self.fdfs_upload(request.data.get('img'))
        return Response({'imgurl': avatar_url})

    def ckeditor_image(self, request):
        image_url = self.fdfs_upload(request.data.get('upload'))
        return redirect(settings.CKEDITOR_URL.format(image_url))

    @staticmethod
    def fdfs_upload(image_file):
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        result = client.upload_appender_by_buffer(image_file.read())
        if result.get('Status') != 'Upload successed.':
            raise APIException('上传文件失败')
        file_name = result.get('Remote file_id')
        return settings.FDFS_URL + file_name