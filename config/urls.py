from django.contrib import admin
from django.urls import path, include
from config.views import indexView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('', indexView, name='index'),
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.instructors.urls')),
    path('', include('apps.courses.urls')),
    path('', include('apps.students.urls')),
    path('', include('apps.lessons.urls')),
    path('', include('apps.progress.urls')),
    path('', include('apps.certificates.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)