from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin_4uck/', admin.site.urls),
    path('auth/', include('authPortal.urls')),
    path('education_counselling_center/', include('education_counselling_center.urls')),
    path('blog/', include('blog.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
