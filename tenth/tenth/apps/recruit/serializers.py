from rest_framework import serializers

from recruit.models import City, Enterprise, Recruit


class HotCitySerializer(serializers.ModelSerializer):
    """热门城市序列化器"""
    class Meta:
        model = City
        fields = '__all__'


class RecruitEnterpriseSerializer(serializers.ModelSerializer):
    """职位企业序列化器"""
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'recruits', 'summary')


class RecruitSerializer(serializers.ModelSerializer):
    """职位序列化器"""
    enterprise = RecruitEnterpriseSerializer(read_only=True)

    class Meta:
        model = Recruit
        fields = ('id', 'jobname', 'salary', 'condition', 'education', 'type', 'city', 'createtime', 'enterprise',
                  'labels')


class EnterpriseSerializer(serializers.ModelSerializer):
    """企业序列化器"""

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'recruits', 'summary')


class EnterpriseDetailSerializer(serializers.ModelSerializer):
    """企业详情序列化器"""
    recruits = RecruitSerializer(many=True, read_only=True)

    class Meta:
        model = Enterprise
        fields = '__all__'


class RecruitDetailSerializer(serializers.ModelSerializer):
    """职位详情序列化器"""
    enterprise = EnterpriseDetailSerializer(read_only=True)

    class Meta:
        model = Recruit
        fields = '__all__'
