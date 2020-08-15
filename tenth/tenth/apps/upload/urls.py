from django.urls import re_path
from upload import views


urlpatterns = [
    re_path('^upload/avatar/$', views.UploadImageViewSet.as_view({
        'post': 'upload_avatar'
    })),
    re_path('^upload/common/$', views.UploadImageViewSet.as_view({
        'post': 'ckeditor_image'
    }))
]