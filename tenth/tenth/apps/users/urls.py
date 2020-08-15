from django.urls import re_path
from users import views
from rest_framework.routers import SimpleRouter


urlpatterns = [
    # 发送短信验证码
    re_path(r'^sms_codes/(?P<mobile>.*)/$', views.SendSMSView.as_view()),
    # 注册用户
    re_path(r'^users/$', views.RegisterView.as_view()),
    # 登陆
    re_path(r'^authorizations/$', views.LoginView.as_view()),
    # 用户详情
    re_path(r'^user/$', views.UserInfoView.as_view()),
    # 用户标签
    re_path(r'^user/label/$', views.UserLabelView.as_view()),
    # 用户关注
    re_path(r'^users/like/(?P<pk>\d+)/$', views.UserLikeView.as_view())

]
