from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_to_video_view, name='image_to_video'),
]