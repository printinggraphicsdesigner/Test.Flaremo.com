from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about),
    path('contact/', views.contact),
    path('privacy-policy/', views.privacy),
    path('terms/', views.terms),
    path('disclaimer/', views.disclaimer),
]