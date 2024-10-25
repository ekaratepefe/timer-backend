# projename/urls.py

from django.contrib import admin
from django.urls import path, include

from TimerProject import views
from TimerProject.views import api_root

urlpatterns = [
    path('', views.redirect_api_root),
    path('api/', views.api_root, name='api-root'), # Add this line to show the API root
    path('admin/', admin.site.urls),  # Admin paneli için yol
    path('', include('app_user.urls')),  # Kullanıcı ile ilgili API yolları
    path('', include('app_timers.urls')),  # Zamanlayıcılar ile ilgili API yolları
    path('', include('app_statistics.urls')),  # İstatistikler ile ilgili API yolları
    path('', include('app_ai.urls')),  # AI ile ilgili API yolları
]
