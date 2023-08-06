
Install:

```
pip install django-mp-seo
```

settings.py:

```
from seo import SeoAppSettings
 
 
class CommonSettings(
        ...
        SeoAppSettings,
        BaseSettings):
    pass
```

urls.py

```
from seo.urls import seo_urlpatterns
 
urlpatterns = [
    ...
] + seo_urlpatterns
```

core/sitemaps.py

```
 
from django.urls import reverse
 
from seo.sitemaps import Sitemap
 
 
class CommonSitemap(Sitemap):
 
    patterns = [
        'example:example'
    ]
 
    def get_extra_urls(self):

        for obj in Example.objects.all():
            yield reverse(
                'example:example', args=[
                    obj.slug, obj.id
                ]
            )

```

templates/sitemap.html
```
 
{% extends 'sitemap.html' %}
 
{% load i18n %}
 
 
{% block items %}
 
    <li>
        <a href="{% url 'example:example' %}">
            {% trans 'Example' %}
        </a>
    </li>
 
{% endblock %}
```

templates/wrapper.html
```
{% load ... seo %}
 
<!DOCTYPE html>
<html lang="en">
 
    <head>
 
        <title>{% block meta_title %}{% get_meta_tag 'title' config.default_title %}{% endblock %}</title>
 
        {% get_meta_tag 'charset' %}
        {% get_meta_tag 'keywords' %}
        {% get_meta_tag 'description' %}
        {% get_meta_tag 'robots' %}
        {% get_meta_tag 'og:image' '/static/img/site-logo.png' %}
 
        {% get_favicon_tag %}
        {% get_viewport_tag %}
        {% get_language_meta_tags %}
        
        ...
 
    </head>
 
    <body {% block body_attrs %}{% endblock %}>
 
        {% block body %}
 
            {% block header %}{% endblock %}
 
            {% block wrapper %}{% endblock %}
 
            {% block footer %}{% endblock %}
 
        {% endblock %}

    </body>
 
    {% block js %}
     
        ...
 
        {% sitemetrics %}
 
    {% endblock %}
 
</html>
```

Run migrations:

```
python manage.py migrate
```

some_app/seo.py


```
# -*- coding: utf-8 -
 
page_meta = [
    {
        'url': '',
        'title': '',
        'title_uk': '',
        'title_ru': '',
        'title_en': '',
        'keywords': '',
        'keywords_uk': '',
        'keywords_ru': '',
        'keywords_en': '',
        'description': '',
        'description_uk': '',
        'description_ru': '',
        'description_en': '',
        'breadcrumb': '',
        'breadcrumb_uk': '',
        'breadcrumb_ru': '',
        'breadcrumb_en': '',
        'header': '',
        'header_uk': '',
        'header_ru': '',
        'header_en': ''
    }
]
 
```

python manage.py sync_page_meta
