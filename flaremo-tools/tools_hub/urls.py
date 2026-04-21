from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('core.urls')),
    path('translator/', include('translator.urls')),
    path('word-to-pdf/', include('word_to_pdf.urls')),
    path('image-to-video/', include('image_to_video.urls')),
    path('image-to-text/', include('image_to_text.urls')),

    path('blog/', include('blog.urls')),
    path('', include('pages.urls')),
    path('account/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)