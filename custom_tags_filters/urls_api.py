from django.urls import path
from rest_framework.routers import DefaultRouter

from . import apiviews

router = DefaultRouter()
router.register('days', apiviews.DayViewSet, base_name='days')

api_patterns = [
    path('photo/', apiviews.profile_picture, name='profile-picture')
] + router.urls
