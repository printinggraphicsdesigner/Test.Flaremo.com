from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')), 
    path('', include('core.urls')),
    path('word-to-pdf/', include('word_to_pdf.urls')),
    path('translator/', include('translator.urls')),  # 👈 ADD
]