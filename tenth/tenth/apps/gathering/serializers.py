from rest_framework import serializers

from gathering.models import Gathering


class GatheringSerializer(serializers.ModelSerializer):
    """活动序列化器"""
    class Meta:
        model = Gathering
        fields = '__all__'
