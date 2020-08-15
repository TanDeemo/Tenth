from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings

from users.models import User
import re


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    token = serializers.CharField(label='JWT Token', read_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'token', 'avatar', 'sms_code')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 16,
                'error_messages': {
                    'min_length': '密码长度为8-16位',
                    'max_length': '密码长度为8-16位'
                }
            },
            'username': {
                'min_length': 5,
                'max_length': 10,
                'error_messages': {
                    'min_length': '用户名长度为5-10位',
                    'max_length': '用户名长度为5-10位'
                }
            }

        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式错误')
        return value

    def validate_username(self, value):
        if re.match(r'^\d+', value):
            raise serializers.ValidationError('用户名不能以数字开头')
        return value

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        client_sms_code = attrs.get('sms_code')

        redis_conn = get_redis_connection('verify_code')
        server_sms_code = redis_conn.get(f'sms_{mobile}')
        if server_sms_code is None or client_sms_code != server_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user


class LoginSerializer(serializers.ModelSerializer):
    """登陆序列化器"""
    token = serializers.CharField(label='JWT Token', read_only=True)
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'avatar', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'mobile': {
                'read_only': True
            },
            'avatar': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        acount = attrs.get('username')
        passowrd = attrs.get('password')

        if re.match(r'^1[3-9]\d{9}$', acount):
            user = User.objects.get(mobile=acount)
        else:
            user = User.objects.get(username=acount)

        if not user.check_password(passowrd):
            raise serializers.ValidationError('用户名或密码错误')

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user



    

