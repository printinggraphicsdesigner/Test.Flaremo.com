from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='account_dashboard'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]