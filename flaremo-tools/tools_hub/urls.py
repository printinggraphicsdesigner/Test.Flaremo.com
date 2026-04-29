from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import login_view, register_view  # only these 2 global

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Auth (global clean URL)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    # ✅ Account system (dashboard, otp, etc)
    path('account/', include('accounts.urls')),

    # ✅ Main apps
    path('', include('core.urls')),
    path('translator/', include('translator.urls')),
    path('word-to-pdf/', include('word_to_pdf.urls')),
    path('image-to-video/', include('image_to_video.urls')),
    path('image-to-text/', include('image_to_text.urls')),
    path('blog/', include('blog.urls')),

    # ✅ Dynamic pages (about, contact, etc)
    path('', include('pages.urls')),
]

# ✅ Media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)