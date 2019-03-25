from rest_framework import serializers

from . import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutMe
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class TimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Timeline
        fields = '__all__'
