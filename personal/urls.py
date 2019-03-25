from django.urls import path, include

from . import views
from . import urls_api

app_name = 'personal'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('portfolio/', views.ProjectListView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('about/', views.AboutMeListView.as_view(), name='about'),
    path('api/', include(urls_api.api_patterns))
]
