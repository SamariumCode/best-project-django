from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('rosetta/', include('rosetta.urls')),
    path('ticket/', include('ticket.urls')),
    path('store/', include('store.urls')),
]

if settings.DEBUG:  # Ensure Debug Toolbar is only added in debug mode
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
