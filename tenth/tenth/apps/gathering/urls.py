from django.urls import re_path
from rest_framework.routers import SimpleRouter

from gathering import views


urlpatterns = [

]

router = SimpleRouter()
router.register('gatherings', views.GatheringViewSet, basename='gather')
urlpatterns += router.urls
