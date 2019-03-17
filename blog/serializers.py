from rest_framework import serializers

from . import models


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscriber
        fields = '__all__'
