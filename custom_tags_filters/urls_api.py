from django.urls import path
from rest_framework.routers import DefaultRouter

from . import apiviews

router = DefaultRouter()
router.register('days', apiviews.DayViewSet, base_name='days')

api_patterns = router.urls
