from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from .models import Spends


class SpendsSerializer(ModelSerializer):
    class Meta:
        model = Spends
        fields = ['payer', 'category', 'cost', 'comment', 'cost_date']


class SpendsGroupedSerializer(Serializer):
    name = serializers.CharField(read_only=True)
    total = serializers.FloatField(read_only=True)
