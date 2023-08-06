
from pydoc import locate

from django.conf import settings
from django.core.management.base import BaseCommand

from modeltranslation.utils import get_translation_fields

from seo.models import PageMeta


class Command(BaseCommand):

    def handle(self, *args, **options):

        for app_name in settings.INSTALLED_APPS:
            self._create_page_meta(app_name)

        self.stdout.write(self.style.SUCCESS('Success'))

    def _create_page_meta(self, app_name):

        meta_list = locate(app_name + '.seo.page_meta')

        if not meta_list:
            return

        for params in meta_list:

            if PageMeta.objects.filter(url=params['url']).exists():
                continue

            record = PageMeta(url=params['url'])

            for f_name in PageMeta.FIELDS_FOR_RENDERING:

                if f_name in params:
                    setattr(record, f_name, params[f_name])

                for trans_field in get_translation_fields(f_name):
                    if trans_field in params:
                        setattr(record, trans_field, params[trans_field])

            record.save()
