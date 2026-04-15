from django.urls import path
from . import views

urlpatterns = [
    path('', views.word_to_pdf_view, name='word_to_pdf'),
]