from django.urls import path

from rest_framework.routers import DefaultRouter

from . import apiviews

router = DefaultRouter()
router.register('entries', apiviews.EntryViewSet, base_name='entries')

api_patterns = [
    path('entries/<int:pk>/comments/', apiviews.CommentsListCreateView.as_view(), name='comments'),
    path('subscribe/', apiviews.SubscriberCreateView.as_view(), name='subscribe'),
    path('archive/', apiviews.ArchiveView.as_view(), name='archive')
]
api_patterns += router.urls
