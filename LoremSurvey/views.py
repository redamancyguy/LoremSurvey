from django.http import JsonResponse, HttpResponse
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'index.html')
        from django.middleware.csrf import get_token
        return JsonResponse({
            'code':0,
            'data2':get_token(request=request)
        })

    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "unknown"
        })


class NotFound(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "Page not found"
        })


    def post(self, request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "unknown"
        })


def test(request):
    print(request.body)
    return HttpResponse('TESTING!!!')


