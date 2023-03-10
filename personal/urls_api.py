from django.urls import path

from rest_framework.routers import DefaultRouter

from . import apiviews

router = DefaultRouter()
router.register('projects', apiviews.ProjectViewSet, base_name='projects')

api_patterns = [
    path('about/', apiviews.AboutMeListView.as_view(), name='about_me'),
    path('timeline/', apiviews.TimelineListView.as_view(), name='timeline'),
    path('contact/', apiviews.MessageCreateView.as_view(), name='contact')
]
api_patterns += router.urls
