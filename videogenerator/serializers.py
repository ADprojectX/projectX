from rest_framework import serializers
from .models import Request, ProjectAssets


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class ProjectAssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAssets
        fields = '__all__'