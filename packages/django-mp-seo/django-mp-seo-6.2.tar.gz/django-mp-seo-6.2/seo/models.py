
from django.db import models
from django.template import Template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class PageMeta(models.Model):

    META_ROBOTS_CHOICES = (
        ('index, follow', _('Index, Follow')),
        ('noindex, nofollow', _('No Index, No Follow')),
        ('index, nofollow', _('Index, No Follow')),
        ('noindex, follow', _('No Index, Follow')),
    )

    FIELDS_FOR_RENDERING = {
        'title', 'keywords', 'description', 'breadcrumb', 'header'}

    url = models.CharField(
        _('URL'), max_length=255, blank=False, unique=True, db_index=True)

    title = models.CharField(_('Title'), max_length=68, blank=False)

    keywords = models.CharField(_('Keywords'), max_length=100, blank=True)

    description = models.CharField(
        _('Description'), max_length=155, blank=True)

    breadcrumb = models.CharField(_('Breadcrumb'), max_length=100, blank=True)

    header = models.CharField(_('Header'), max_length=100, blank=True)

    og_image = models.CharField(_('og:image'), max_length=500, blank=True)

    robots = models.CharField(
        _('Robots'), max_length=30, blank=True, default='index, follow',
        choices=META_ROBOTS_CHOICES)

    def render(self, field_name, context, default=''):

        if field_name == 'charset':
            return mark_safe('<meta charset="utf-8">')

        if field_name == 'robots':
            return self._render_meta_tag(field_name, self.robots)

        if field_name == 'og:image':
            return self.render_og_image_tag(context, default)

        if field_name not in self.FIELDS_FOR_RENDERING:
            raise ValueError

        value = getattr(self, field_name)

        if not value:
            return default

        value = self._render_value(value, context)

        if field_name in ['keywords', 'description']:
            return self._render_meta_tag(field_name, value)

        return value

    def render_og_image_tag(self, context, default):

        if self.og_image:
            og_image = self._render_value(self.og_image, context)
        else:
            og_image = default

        try:
            return mark_safe(
                """
                    <meta property="og:image" 
                          content="https://{}{}">
                """.format(
                    context.request.META['HTTP_HOST'],
                    og_image
                )
            )
        except Exception as e:
            print(e)
            return ''

    def _render_value(self, value, context):
        return Template(value).render(context)

    def _render_meta_tag(self, field_name, value):
        return mark_safe(
            '<meta name="{}" content="{}">'.format(field_name, value)
        )

    def __str__(self):
        return '{} - {}'.format(self.url, self.title)

    class Meta:
        verbose_name = _('Page meta')
        verbose_name_plural = _('Pages meta')


class RedirectRecord(models.Model):

    old_path = models.CharField(
        _('Old path'), max_length=1024, db_index=True, unique=True)

    new_path = models.CharField(_('New path'), max_length=1024)

    def __str__(self):
        return self.old_path

    class Meta:
        verbose_name = _('Redirect record')
        verbose_name_plural = _('Redirect records')


class ErrorRecord(models.Model):

    path = models.CharField(_('Path'), max_length=1024, db_index=True)

    referrer = models.CharField(_('Referrer'), max_length=1024, blank=True)

    status_code = models.IntegerField(_('Status code'))

    created = models.DateTimeField(_('Creation date'), auto_now_add=True)

    method = models.CharField(_('Method'), max_length=100)

    def __str__(self):
        return '[{}] {}'.format(str(self.status_code).upper(), self.path)

    @classmethod
    def create(cls, request, status_code):
        return cls.objects.create(
            path=request.get_full_path(),
            status_code=status_code,
            method=request.method,
            referrer=request.META.get('HTTP_REFERER', ''))

    class Meta:
        verbose_name = _('Error record')
        verbose_name_plural = _('Error records')


class SearchQuery(models.Model):

    query = models.CharField(
        _('Query'), max_length=255, blank=True)

    result_count = models.IntegerField(
        _('Result count'))

    filter_options = models.TextField(
        _('Filter options'), max_length=2000, blank=True)

    created = models.DateTimeField(
        _('Created'), auto_now_add=True)

    def __str__(self):
        return str(self.created)

    class Meta:
        verbose_name = _('Search query')
        verbose_name_plural = _('Search queries')
