from django.urls import path, include

from . import views
from . import urls_api

app_name = 'blog'
urlpatterns = [
    path('', views.EntryListView.as_view(), name='index'),
    path('detail/<int:pk>/', views.EntryDetailView.as_view(), name='detail'),
    path('api/', include(urls_api.api_patterns))
]
