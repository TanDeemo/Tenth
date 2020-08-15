from django.urls import re_path
from rest_framework.routers import SimpleRouter

from question import views


urlpatterns = [

]

router = SimpleRouter()
router.register('labels', views.LabelViewSet, basename='labels')
router.register('questions', views.QuestionViewSet, basename='questions')
router.register('reply', views.ReplyViewSet, basename='reply')
urlpatterns += router.urls


