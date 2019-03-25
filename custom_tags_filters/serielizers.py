from rest_framework import serializers

from . import models


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = '__all__'
