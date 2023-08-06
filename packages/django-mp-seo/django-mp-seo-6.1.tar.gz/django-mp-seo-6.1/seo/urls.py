
from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from seo.views import sitemap_download, sitemap_tree


seo_urlpatterns = [
    path('sitemap.xml', sitemap_download)
]

seo_urlpatterns += i18n_patterns(
    path('sitemap/', sitemap_tree, name='sitemap-tree'),
)
