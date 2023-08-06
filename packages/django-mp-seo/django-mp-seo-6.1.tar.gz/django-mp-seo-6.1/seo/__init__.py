
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from seo.settings import SeoAppSettings


class SeoConfig(AppConfig):
    name = 'seo'
    verbose_name = _("SEO")


default_app_config = 'seo.SeoConfig'
