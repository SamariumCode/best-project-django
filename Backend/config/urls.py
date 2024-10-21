from django.contrib import admin
from django.conf import settings
from django.urls import path, include
import debug_toolbar
from store.views import home
from django.views import defaults as default_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('store/home/', home, name='home'),
    # path('500/', default_views.server_error, name='server_error'),
]

if settings.DEBUG:  # Ensure Debug Toolbar is only added in debug mode
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
