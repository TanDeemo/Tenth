from django.urls import re_path
from headline import views
from rest_framework.routers import SimpleRouter


urlpatterns = [

]

router = SimpleRouter()
router.register('channels', views.ChannelsViewSet, basename='channels')
router.register('article', views.ArticleViewSet, basename='headline')
router.register('articles/search', views.ArticleSearchView, basename='articles_search')
urlpatterns += router.urls