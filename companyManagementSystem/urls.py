from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
        path('admin/', admin.site.urls),

        path('api/v1/', include([
            path('schema/', SpectacularAPIView.as_view(), name='schema'),
            path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('auth/', include('users.urls')),
            path('projects/', include('projects.urls')),
            path('organizations/', include('organizations.urls')),
            path('performance/', include('performance.urls')),
            ])
        )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]