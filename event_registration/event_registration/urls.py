import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('events.urls')),
                  path('', include('participants.urls')),
                  path('', include('CRM.urls')),
                  path('', RedirectView.as_view(url='events_list/')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),

        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
