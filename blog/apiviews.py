from django.utils import timezone
from django.conf import settings
from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from . import models
from .signals import subscriber_created
from .signals import comment_created


class EntryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.EntrySerializer
    permission_classes = ()

    def get_queryset(self):
        queryset = models.Entry.objects.filter(status='PB')
        search_query = self.request.GET.get('q')
        if search_query:
            return queryset.filter(headline__icontains=search_query)
        return queryset


class CommentsListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = ()

    def get_queryset(self):
        queryset = models.Comment.objects.filter(entry_id=self.kwargs['pk'])
        return queryset.order_by('-when')

    def create(self, request, **kwargs):
        data = request.data
        model_data = {'entry': kwargs['pk'],
                      'full_name': data['full_name'],
                      'email': data['email'],
                      'content': data['content'],
                      'when': timezone.now()}
        serializer = self.serializer_class(data=model_data)
        entry = models.Entry.objects.get(id=self.kwargs['pk'])
        if entry.status == 'PB':
            if serializer.is_valid():
                serializer.save()
                comments = models.Comment.objects.filter(entry_id=kwargs['pk'])
                comment_created.send(self.__class__, comments=comments,
                                     who_commented=data['email'], entry=entry)
                return Response(data=self.serializer_class(instance=comments,
                                                           many=True).data,
                                status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail': 'You cannot create a comment in this unpublished article.'},
                            status=status.HTTP_400_BAD_REQUEST)


class SubscriberCreateView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = serializers.SubscriberSerializer

    def create(self, request, **kwargs):
        data = request.data
        model_data = {'email': data['email']}
        serializer = self.serializer_class(data=model_data)
        if serializer.is_valid():
            serializer.save()
            subscriber_created.send(self.__class__, email=data['email'])
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'details': 'Subscriber with this email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ArchiveView(views.APIView):
    permission_classes = ()

    @staticmethod
    def get(request):
        ar = {}
        entries = models.Entry.objects.filter(
            status='PB').order_by('pub_date__year')
        for entry in entries:
            if entry.pub_date.year not in ar:
                year = entry.pub_date.year
                ar[year] = {}
                for i in entries.filter(pub_date__year=year):
                    if i.pub_date.strftime('%B') not in ar[year]:
                        month = i.pub_date.strftime('%B')
                        ar[year][month] = []
                        for e in entries.filter(pub_date__year=year, pub_date__month=i.pub_date.month):
                            ar[year][month].append(
                                [e.id, str(e.pub_date.day), e.headline])
        return Response(data=ar, status=status.HTTP_200_OK)

