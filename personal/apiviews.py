"""API views of personal"""

import json
import requests
from pprint import pprint

from django.utils import timezone
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import views
from rest_framework import generics
from rest_framework import status

from . import models
from . import serializers


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ProjectSerializer
    permission_classes = ()

    def get_queryset(self):
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('q')

        # listing category
        if category:
            return models.Project.objects.filter(category=category.lower())
        # listing search results
        elif search_query:
            return models.Project.objects.filter(name__icontains=search_query)
        # listing all
        else:
            return models.Project.objects.all()


class AboutMeListView(generics.ListAPIView):
    permission_classes = ()
    queryset = models.AboutMe.objects.all()
    serializer_class = serializers.AboutMeSerializer


class TimelineListView(generics.ListAPIView):
    permission_classes = ()
    queryset = models.Timeline.objects.all().order_by('-date')
    serializer_class = serializers.TimelineSerializer


class MessageCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = serializers.CommentSerializer

    def create(self, request, **kwargs):
        data = request.data
        model_data = {'full_name': data['full_name'],
                      'email': data['email'],
                      'content': data['content'],
                      'date_time': timezone.now()}
        serializer = self.serializer_class(data=model_data)
        if serializer.is_valid():
            # Email myself
            subject = 'Somebody sent you a message'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [from_email]
            contact_message = f"{model_data['full_name']} said:\n{model_data['content']}"
            send_mail(subject, contact_message, from_email, to_email)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
