from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')

    def post(self,request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "unknown"
        })


class NotFound(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>page not found</h1>')

    def post(self,request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': "unknown"
        })


