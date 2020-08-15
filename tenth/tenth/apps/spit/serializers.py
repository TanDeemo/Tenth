from rest_framework_mongoengine import serializers

from spit.models import Spit


class SpitSerializer(serializers.DocumentSerializer):
    """吐槽序列化器"""
    class Meta:
        model = Spit
        fields = '__all__'
        extra_kwargs = {
            'content': {
                'required': True
            }
        }
