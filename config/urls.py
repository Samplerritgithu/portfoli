from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import StaticViewSitemap
from apps.core.views import health, home, manifest, service_worker

sitemaps = {'static': StaticViewSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
    path('', home, name='home'),
    path('blog/', include('apps.blog.urls')),
    path('api/v1/', include('apps.api.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('manifest.json', manifest, name='manifest'),
    path('sw.js', service_worker, name='service_worker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Shiva Shankar Chanda — Portfolio Admin'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Dashboard'
