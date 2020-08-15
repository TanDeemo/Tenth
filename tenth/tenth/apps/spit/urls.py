from django.urls import re_path
from rest_framework.routers import SimpleRouter

from spit import views


urlpatterns = [

]

router = SimpleRouter()
router.register('spit', views.SpitViewSet, basename='spit')
urlpatterns += router.urls
