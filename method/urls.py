from django.contrib import admin
from django.urls import path

from .views import UserRegistrationView, UserLoginView, OTPVerificationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', UserLoginView.as_view(), name ='user_login'),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp_verification'),
]