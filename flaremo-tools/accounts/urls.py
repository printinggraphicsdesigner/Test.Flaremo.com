from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='account_dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # OTP
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),

    # Password reset
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
