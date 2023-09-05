from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('events.urls')),
                  # path('', include('participants.urls')),
                  path('', include('events.urls')),
                  path('', RedirectView.as_view(url='events_list/')),
                  path('accounts/', include('django.contrib.auth.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
