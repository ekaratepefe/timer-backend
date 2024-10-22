# app_statistics/urls.py

from django.urls import path
from .views import StatisticsDashboardView

urlpatterns = [
    path('dashboard/', StatisticsDashboardView.as_view(), name='statistics_dashboard'),  # İstatistik dashboard API'si
]
