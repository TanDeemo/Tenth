from django.urls import re_path
from users import views


urlpatterns = [
    # 发送短信验证码
    re_path(r'^sms_codes/(?P<mobile>.*)/$', views.SendSMSView.as_view()),
    # 注册用户
    re_path(r'^users/$', views.RegisterView.as_view()),
    # 登陆
    re_path(r'^authorizations/$', views.LoginView.as_view())
]