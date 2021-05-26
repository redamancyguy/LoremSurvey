from django.utils.deprecation import MiddlewareMixin


class Custom(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # return callback(request, *callback_args, **callback_kwargs)
        pass

    @staticmethod
    def process_exception(request, exception):
        pass

    @staticmethod
    def process_response(request, response):
        return response

    @staticmethod
    def process_template_response(request, response):
        print('this')
        return response
