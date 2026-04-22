from django.urls import path
from . import views

urlpatterns = [
    path('', views.translator_view, name='translator'),
]