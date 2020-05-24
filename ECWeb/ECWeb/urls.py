from django.urls import path, include
from baton.autodiscover import admin
from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView
from django.conf.urls.static import static





urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', include('core.urls', namespace = 'core')),
    path('accounts/', include('allauth.urls')),
    url(r'^baton/', include('baton.urls')),
    path(r'favicon.ico', RedirectView.as_view(url=r'/img/favicon.ico')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
