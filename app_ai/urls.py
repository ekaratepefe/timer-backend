# app_ai/urls.py

from django.urls import path
from .views import AIPromptView

urlpatterns = [
    path('prompt/', AIPromptView.as_view(), name='ai_prompt_view'),  # API endpoint
]
