from django.urls import path, include

from . import views
from . import urls_api

app_name = 'custom_tags_filters'

urlpatterns = [
    path('api/', include(urls_api.api_patterns))
]
