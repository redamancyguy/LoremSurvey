from django.http import QueryDict
import json
try:
    from django.utils.deprecation import MiddlewareMixin  # 1.10.x
except ImportError:
    MiddlewareMixin = object  # 1.4.x-1.9.x


class HttpPost2HttpOtherMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        """
        可以继续添加HEAD、PATCH、OPTIONS以及自定义方法
        HTTP_X_METHODOVERRIDE貌似是以前版本的key？？？
        :param request: 经过原生中间件处理过后的请求
        :return:
        """
        try:
            http_method = request.META['REQUEST_METHOD']
            if http_method.upper() not in ('GET', 'POST'):
                setattr(request, http_method.upper(), QueryDict(request.body))
        except Exception as e:
            print('error', e)
        finally:
            return None
