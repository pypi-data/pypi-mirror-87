
from django.template import Library
from django.utils.safestring import mark_safe


register = Library()


@register.simple_tag(takes_context=True)
def get_meta_tag(context, field_name, default=''):
    page_meta = context.request.page_meta
    return page_meta.render(field_name, context, default)


@register.inclusion_tag('language_meta_tags.html', takes_context=True)
def get_language_meta_tags(context):
    return context


@register.simple_tag
def get_viewport_tag(content=None):

    if content is None:
        content = 'width=device-width,initial-scale=1'

    return mark_safe('<meta name="viewport" content="{}" />'.format(content))


@register.simple_tag(takes_context=True)
def get_favicon_tag(context, path=None):

    if path is None:
        path = context['STATIC_URL'] + 'img/favicon.ico'

    return mark_safe('<link rel="shortcut icon" href="{}">'.format(path))


@register.inclusion_tag('sitemetrics_tag.html', takes_context=True)
def sitemetrics(context):
    return context
