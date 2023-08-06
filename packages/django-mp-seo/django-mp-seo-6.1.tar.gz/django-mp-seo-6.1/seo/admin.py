
from django.apps import apps
from django.contrib import admin

from seo.models import PageMeta, RedirectRecord, ErrorRecord, SearchQuery


def _get_page_meta_parent_admin_classes():

    if apps.is_installed('modeltranslation'):
        from modeltranslation.admin import TranslationAdmin
        classes = [TranslationAdmin]
    else:
        classes = [admin.ModelAdmin]

    if apps.is_installed('import_export'):

        from import_export.resources import ModelResource
        from import_export.admin import ImportExportMixin, ExportActionMixin

        class PageMetaResource(ModelResource):
            class Meta:
                model = PageMeta
                exclude = ('id', )

        class ImportExportAdmin(
                ImportExportMixin,
                ExportActionMixin):

            actions_on_bottom = False
            resource_class = PageMetaResource

        classes.append(ImportExportAdmin)

    return classes


@admin.register(PageMeta)
class PageMetaAdmin(*_get_page_meta_parent_admin_classes()):

    list_display = ['url', 'title', 'robots']
    list_editable = ['robots']
    list_filter = ['robots']
    search_fields = ['url', 'title']


@admin.register(RedirectRecord)
class RedirectRecordAdmin(admin.ModelAdmin):

    list_display = ['id', 'old_path', 'new_path']
    list_display_links = ['old_path', 'new_path']
    search_fields = ['old_path', 'new_path']


@admin.register(ErrorRecord)
class ErrorRecordAdmin(admin.ModelAdmin):

    list_display = [
        'id', 'path', 'method', 'status_code', 'referrer', 'created']
    list_display_links = ['path']
    search_fields = ['path']
    list_filter = ['status_code']


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['created', 'query', 'filter_options', 'result_count']
    search_fields = ['query', 'filter_options']
