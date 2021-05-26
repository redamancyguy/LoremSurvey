from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.cache import cache_page

from . import models


class ResetCookies(MiddlewareMixin):

    def process_request(self, request):
        pass

    @staticmethod
    @cache_page(60 * 15)
    def process_response(request, response):
        info = models.User.objects.filter(token=request.COOKIES.get('token')).first()
        if info and request.COOKIES.get('token') != '':
            response.set_cookie('token', request.COOKIES.get('token'), max_age=1800)
        return response

