from django.urls import path
from .views import page_detail

urlpatterns = [
    path('page/<slug:slug>/', page_detail),

    # 👇 short URLs
    path('about/', page_detail, {'slug': 'about'}),
    path('contact/', page_detail, {'slug': 'contact'}),
    path('privacy/', page_detail, {'slug': 'privacy'}),
    path('terms/', page_detail, {'slug': 'terms'}),
    path('disclaimer/', page_detail, {'slug': 'disclaimer'}),
]