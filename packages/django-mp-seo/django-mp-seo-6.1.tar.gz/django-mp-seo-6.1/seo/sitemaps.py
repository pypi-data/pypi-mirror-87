
from django.apps import apps
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from django.utils.translation import activate
from django.contrib.sitemaps import Sitemap as DjangoSitemap


class Sitemap(DjangoSitemap):

    changefreq = 'monthly'
    priority = 1.0
    patterns = []

    def items(self):

        urls = []

        for lang_code, lang_name in settings.LANGUAGES:

            activate(lang_code)

            urls += list(self.get_extra_urls())

            if apps.is_installed('flatpages'):
                from flatpages.models import FlatPage
                for fp in FlatPage.objects.all():
                    urls.append(
                        reverse('flatpages:page', kwargs={'url': fp.url}))

            for pattern in self.patterns:
                urls.append(reverse(pattern))

            try:
                urls.append(reverse('sitemap-tree'))
            except Exception:
                pass

        return urls

    def get_extra_urls(self):
        return []

    def location(self, obj):
        return obj

    def lastmod(self, obj):
        return datetime.now()
