
from seo.lib import get_page_meta


class PageMetaMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        request.page_meta = get_page_meta(request)

        return self.get_response(request)
