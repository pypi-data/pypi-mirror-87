
from django.shortcuts import render, redirect, Http404
from django.contrib.sitemaps.views import sitemap

from seo.models import RedirectRecord, ErrorRecord


def sitemap_download(request):
    try:
        from core.sitemaps import CommonSitemap
        return sitemap(request, {'generic': CommonSitemap})
    except ImportError:
        return Http404()


def sitemap_tree(request):
    return render(request, 'sitemap.html')


def page_not_found(request, **kwargs):

    path = request.path

    try:
        record = RedirectRecord.objects.get(old_path=path)
        return redirect(record.new_path, permanent=True)
    except RedirectRecord.DoesNotExist:
        pass

    if not path.startswith('/static/') and not path.startswith('/media/'):
        ErrorRecord.create(request, 404)

    return render(request, '404.html')
