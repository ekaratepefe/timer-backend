# app_user/urls.py

from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('api/user/register/', views.RegisterUserView.as_view(), name='register'),
    path('api/login-with-session/', login_view, name='login-with-session'),

    path('api/user/login-with-token/', views.LoginView.as_view(), name='login-with-token'),
    path('api/user/logout/', views.LogoutView.as_view(), name='logout'),
    path("api/user/email/verification/send-code", views.SendVerifyCodeView.as_view(), name='send-email-verify-code'),
    path("api/user/email/verification/confirm-code", views.VerifyCodeView.as_view(), name='confirm-email-verify-code'),
    path('payment/', views.PaymentView.as_view(), name='make_payment'),
]
# urls.py

from django.urls import path
