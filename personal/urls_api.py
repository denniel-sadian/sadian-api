from django.urls import path

from rest_framework.routers import DefaultRouter

from . import apiviews

router = DefaultRouter()
router.register('projects', apiviews.ProjectViewSet, base_name='projects')
router.register('days', apiviews.DayViewSet, base_name='days')

api_patterns = [
    path('about/', apiviews.AboutMeListView.as_view(), name='about_me'),
    path('contact/', apiviews.MessageCreateView.as_view(), name='contact')
]
api_patterns += router.urls
