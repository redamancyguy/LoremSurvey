from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'index.html')
        from django.middleware.csrf import get_token
        return JsonResponse({
            'code': 0,
            'data2': get_token(request=request)
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


class Foo:
    def __init__(self, request):
        self.request = request

    @staticmethod
    def render():
        return HttpResponse('class render')


from question.models1 import M


def test(request):
    for i in M.getDatabase('user', '123456789', 'test').test.find():
        print(i)
    print('==================')
    for i in M.getDatabase('root', 'zxc.cf.1213', 'test1').test.find():
        print(i)
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        print(request)
        print(request.POST)
        print(request.body)
        return JsonResponse({'code': 0, 'msg': 'ok'})
    # return Foo(request).render()
    # return HttpResponse('ok')
