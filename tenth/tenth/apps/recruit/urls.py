from django.urls import re_path
from rest_framework.routers import SimpleRouter

from recruit import views

urlpatterns = [

]

router = SimpleRouter()
router.register('city/hotlist', views.HotCityViewSet, basename='hot_city')
router.register('enterprise', views.EnterpriseViewSet, basename='enterprise')
router.register('recruits', views.RecruitsViewSet, basename='recruit')
urlpatterns += router.urls
