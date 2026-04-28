from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, register_view

from accounts.views import login_view, register_view, verify_otp # এখানে verify_otp যোগ করা হয়েছে

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify-otp/<int:user_id>/', verify_otp, name='verify_otp'),
    path('account/', include('accounts.urls')),
    path('', include('core.urls')),
    path('translator/', include('translator.urls')),
    path('word-to-pdf/', include('word_to_pdf.urls')),
    path('image-to-video/', include('image_to_video.urls')),
    path('image-to-text/', include('image_to_text.urls')),
    path('blog/', include('blog.urls')),
    path('', include('pages.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)