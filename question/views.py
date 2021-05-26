import hashlib
import json
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page

from . import models
from .utils import sendEmail
import threading
import user.models as u_models
import pandas as pd

Domain = 'http://1506607292.top'


def timeCompare(ormTime):
    from datetime import datetime
    if ormTime.year > datetime.now().year:
        return True
    elif ormTime.year == datetime.now().year:
        if ormTime.month > datetime.now().month:
            return True
        elif ormTime.month == datetime.now().month:
            if ormTime.day > datetime.now().day:
                return True
            elif ormTime.day == datetime.now().day:
                if ormTime.hour > datetime.now().hour:
                    return True
                elif ormTime.hour == datetime.now().hour:
                    if ormTime.minute > datetime.now().minute:
                        return True
                    elif ormTime.minute == datetime.now().minute:
                        if ormTime.second > datetime.now().second:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


class Index(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return JsonResponse({'code': 0, 'message': 'Index'})

    @staticmethod
    def post(request, *args, **kwargs):
        return JsonResponse({'code': 0, 'message': 'Index'})


class ControlView(object):
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('token'):
            from user import models as u_model
            if u_model.User.objects.filter(token=request.COOKIES.get('token')).first():
                return super().dispatch(request, *args, **kwargs)
            return JsonResponse({
                'code': 1,
                'message': 'wrong token && please Log in again'
            })
        else:
            return JsonResponse({
                'code': 1,
                'message': 'you do not have token,please login'
            })


class Respondents(ControlView, View):

    @staticmethod
    def get(request, *args, **kwargs):
        userList = []
        for i in models.Respondent.objects.filter(user__token=request.COOKIES.get('token')):
            userList.append(
                {'id': i.sid, 'name': i.name, 'school': i.school, 'phone': i.phone, 'email': i.email, 'sex': i.sex})
        return JsonResponse({
            'code': 0,
            'data': userList,
            'message': 'userList'
        })

    @staticmethod
    def post(request, *args, **kwargs):
        files = request.FILES
        if files:
            print(files)
            for i in files:
                print(i)
            try:
                for i in files:
                    file = request.FILES[i]
                    if file:
                        f = open('./files/' + i, 'wb')
                        for chunk in file.chunks():
                            f.write(chunk)
                        f.close()
                        data = pd.read_excel('./files/' + i).values
                        token = request.COOKIES.get('token')
                        user = u_models.User.objects.filter(token=token).first()
                        for ii in data:
                            models.Respondent.objects.update_or_create(sid=ii[0], user=user, defaults={
                                'name': ii[1], 'school': ii[2],
                                'major': ii[3], 'Class': ii[4], 'sex': ii[5],
                                'phone': ii[6], 'email': ii[7],
                            })
                        os.remove('./files/' + i)
                        return JsonResponse({
                            'code': 0,
                            'message': "Received"
                        })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
            return JsonResponse({
                'code': 2,
                'message': "File transfer but did not receive"
            })
        else:
            return JsonResponse({
                'code': 2,
                'message': "No file transfer"
            })

    @staticmethod
    def delete(request, *args, **kwargs):
        try:
            for i in json.loads(request.body):
                models.Respondent.objects.filter(sid=i).delete()
            return JsonResponse({
                'code': 0,
                'message': "delete successfully"
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e),
            })

    @staticmethod
    def put(request, *args, **kwargs):
        return JsonResponse({
            'code': 2,
            'message': 'change respondents'
        })


class ManageQuestion(ControlView, View):

    @staticmethod
    def get(request, *args, **kwargs):
        if request.GET.get('id') is None:
            try:
                result = []
                token = request.COOKIES.get('token')
                pages = models.Page.objects.filter(user__token=token)
                for i in pages:
                    status = None
                    if i.startTime is None and i.stopTime is None:
                        result.append(
                            {'id': i.id, 'title': i.title, 'desc': i.desc, 'startTime': i.startTime,
                             'stopTime': i.stopTime,
                             'emailTemplate': i.emailTemplate, 'running': i.running,
                             'open': i.open, 'status': status})
                        continue
                    if timeCompare(i.stime):
                        status = '-1'
                    elif not timeCompare(i.etime):
                        status = '1'
                    else:
                        status = '0'
                    result.append(
                        {'id': i.id, 'title': i.title, 'desc': i.desc, 'startTime': i.startTime, 'stopTime': i.stopTime,
                         'emailTemplate': i.emailTemplate, 'running': i.running,
                         'open': i.open, 'status': status})
                return JsonResponse({
                    'code': 0,
                    'data': result,
                    'message': 'get success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
        else:
            result = {}
            try:
                item = models.Page.objects.filter(id=request.GET.get('id')).first()
                if item is None:
                    return JsonResponse({
                        'code': 0,
                        'message': 'None question page id is :' + request.GET.get('id')
                    })
                result['title'] = item.title
                result['open'] = item.open
                result['desc'] = item.desc
                result['startTime'] = item.startTime
                result['stopTime'] = item.stopTime
                result['running'] = item.running
                result['emailTemplate'] = item.emailTemplate
                result['problemSet'] = []
                for i in models.Question.objects.filter(page=item):
                    question = {'index': i.index, 'type': i.type, 'title': i.title, 'desc': i.desc, 'need': i.need,
                                'options': None}
                    if i.type is True:
                        question['options'] = []
                        for ii in models.Choice.objects.filter(question=i):
                            question['options'].append({"label": ii.text, "value": ii.option})
                    result['problemSet'].append(question)
                return JsonResponse({
                    'code': 0,
                    'data': result,
                    'message': 'send success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e),
                })

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            token = request.COOKIES.get('token')
            data = json.loads(request.body.decode())
            user = u_models.User.objects.filter(token=token).first()
            data['open'] = True  # //
            data['running'] = True
            data['startTime'] = None
            data['stopTime'] = None
            page = models.Page.objects.create(title=data['title'], open=data['open'], desc=data['desc'],
                                              emailTemplate=data['emailTemplate'], running=data['running'],
                                              startTime=data['startTime'], stopTime=data['stopTime'], user=user)
            for i in data['problemSet']:
                question = models.Question.objects.create(type=i['type'], index=i['index'], title=i['title'],
                                                          desc=i['desc'], need=i['need'], page=page, )
                if i['type'] is True:
                    for ii in i['options']:
                        models.Choice.objects.create(option=str(ii['value']), text=ii['label'], question=question)
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })
        return JsonResponse({
            'code': 0,
            'message': "Receive questions success",
            'data': {'id': page.id}
        })

    @staticmethod
    def delete(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        data = json.loads(request.body)
        for i in models.Page.objects.filter(id=data['id'], user__token=token):
            i.delete()
            return JsonResponse({
                'code': 0,
                'message': "Delete questions success"
            })
        return JsonResponse({
            'code': 2,
            'message': "None questions to delete"
        })

    @staticmethod
    def put(request, *args, **kwargs):
        data = json.loads(request.body)
        token = request.COOKIES.get('token')
        user = u_models.User.objects.filter(token=token).first()
        pid = data['id']
        data = json.loads(request.body.decode())
        try:
            pages = models.Page.objects.update_or_create(id=pid, user=user, defaults={
                'title': data['title'], 'open': data['open'],
                'desc': data['desc'],
                'emailTemplate': data['emailTemplate'], 'running': data['running'],
                'startTime': data['startTime'], 'stopTime': data['stopTime'],
            })
            page = pages[0]
            # try:
            #     item = models.U_P.objects.filter(pid=pid).first()
            #     item.nums = 0
            #     item.save()
            # except Exception as e:
            #     print(e)
            # for i in pid.fquestion_set.all():
            #     i.delete()
            # for i in pid.cquestion_set.all():
            #     i.delete()
            try:
                for i in data['problemSet']:
                    question = models.Question.objects.update_or_create(page=page, index=i['index'], type=i['type'],
                                                                        defaults={'title': i['title'],
                                                                                  'need': i['need'],
                                                                                  'desc': i['desc']})[0]
                    if i['type'] is True:
                        for j in i['options']:
                            models.Choice.objects.update_or_create(question=question, option=str(j['value']),
                                                                   defaults={'text': j['label']})
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': 'something wrong with problemSet ' + str(e)
                })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': 'something wrong with your question page ' + str(e)
            })
        return JsonResponse({
            'code': 0,
            'message': 'the page ' + str(data['title']) + ' is changed'
        })


class Generate(ControlView, View):

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            pid = request.GET.get('id')
            userList = []
            token = request.COOKIES.get('token')
            for i in models.Respondent.objects.filter(user__token=token):
                status = 0
                if models.Entrance.objects.filter(page__id=pid, respondent=i).first():
                    status = 1
                userList.append(
                    {'id': i.sid, 'name': i.name, 'school': i.school, 'phone': i.phone, 'email': i.email, 'sex': i.sex,
                     'status': status})
            if models.Page.objects.filter(id=pid).first().isopen is True:
                for i in userList:
                    i['status'] = 1
            return JsonResponse({
                'code': 0,
                'data': userList,
                'message': 'respondentsList'
            })
        except Exception as e:
            return JsonResponse({
                'code': 0,
                'message': str(e)
            })

    @staticmethod
    def post(request, *args, **kwargs):
        data = json.loads(request.body)
        pid = data['id']
        userList = data['userList']
        try:
            page = models.Page.objects.filter(id=pid).first()
            if page.isopen is False:
                token = request.COOKIES.get('token')
                flag = False
                for i in models.Respondent.objects.filter(user__token=token, sid__in=userList):
                    flag = True
                    sessionUrl = hashlib.md5((str(page.id) + str(i.id)).encode('utf-8')).hexdigest()
                    try:
                        models.Entrance.objects.create(page=page, respondent=i, sessionurl=sessionUrl, status=False)
                    except Exception as e:
                        print('error:', e)
                    item = threading.Thread(target=sendEmail, args=(i.email, 'The close question URL for you',
                                                                    i.emailTemplate + '      ' + Domain + '/survey/' + sessionUrl))
                    item.start()
                if flag is False:
                    return JsonResponse({
                        'code': 2,
                        'message': 'None people to generate',
                    })
                return JsonResponse({
                    'code': 0,
                    'message': 'Generate Closed source success',
                })
            elif page.isopen is True:
                sessionUrl = hashlib.md5((str(page.id)).encode('utf-8')).hexdigest()
                item = models.Entrance.objects.filter(sessionUrl=sessionUrl, page=page).first()
                token = request.COOKIES.get('token')
                if item:
                    for i in models.Respondent.objects.filter(user__token=token, sid__in=userList):
                        item = threading.Thread(target=sendEmail, args=(i.email, 'The open question URL for you',
                                                                        page.emailTemplate + '      ' + Domain + '/survey/' + sessionUrl))
                        item.start()
                    return JsonResponse({
                        'code': 0,
                        'message': 'Generate open source success you have send the email',
                        'data': {'link': Domain + '/survey/' + str(item.sessionUrl
                                                                   )}
                    })
                for i in models.Respondent.objects.filter(user__token=token, sid__in=userList):
                    item = threading.Thread(target=sendEmail, args=(i.email, 'The open question URL for you',
                                                                    page.emailTemplate + '      ' + Domain + '/survey/' + sessionUrl))
                    item.start()
                models.Entrance.objects.create(respondent=None, page=page, sessionUrl=sessionUrl, status=False)
                return JsonResponse({
                    'code': 0,
                    'message': 'Generate open source success',
                    'data': {'link': Domain + '/survey/' + sessionUrl}
                })
            return JsonResponse({
                'code': 2,
                'message': "Nothing to generate"
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })


class AnswerQuestion(View):

    @staticmethod
    def get(request, *args, **kwargs):
        sessionUrl = request.GET.get('sessionUrl')
        if sessionUrl:
            try:
                data = {}
                item = models.Entrance.objects.filter(sessionUrl=sessionUrl).first()
                if not item:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 105},
                        'message': "Invalid sessionUrl"
                    })
                if item.status is True:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 104},
                        'message': 'you have answer this question'
                    })
                page = item.page
                data['title'] = page.title
                data['open'] = page.open
                data['desc'] = page.desc
                data['startTime'] = page.startTime
                data['stopTime'] = page.stopTime
                data['emailTemplate'] = page.emailTemplate
                data['running'] = page.running
                data['problemSet'] = []
                if data['running'] is False:
                    return JsonResponse({
                        'code': 2,
                        'data': {'statusCode': 100},
                        'message': 'is not running'
                    })
                if page.startTime is not None or page.stopTime is not None:
                    if not timeCompare(page.stopTime):
                        return JsonResponse({
                            'code': 2,
                            'data': {'statusCode': 101},
                            'message': 'The questionnaire time is over'
                        })
                    if timeCompare(page.startTime):
                        return JsonResponse({
                            'code': 2,
                            'data': {'statusCode': 102},
                            'message': 'The questionnaire has not started yet'
                        })
                for i in models.Question.objects.filter(page=page):
                    options = []
                    question = {'index': i.index, 'type': i.type, 'title': i.title, 'need': i.need,
                                'options': options}
                    for ii in models.Choice.objects.filter(question=i):
                        options.append({"label": ii.text, "value": ii.option})
                    data['problemSet'].append(question)
                data['statusCode'] = 103
                return JsonResponse({
                    'code': 0,
                    'data': data,
                    'message': 'send success'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
        else:
            return JsonResponse({
                'code': 2,
                'message': 'Give me you sessionUrl and I will give you the questions'
            })

    @staticmethod
    def post(request, *args, **kwargs):
        sessionUrl = request.GET.get('sessionUrl')
        data = json.loads(request.body.decode())
        item = models.Entrance.objects.filter(sessionUrl=sessionUrl).first()
        if not item:
            return JsonResponse({
                'code': 2,
                'message': 'Invalid sessionUrl'
            })
        page = item.page
        respondent = item.respondent
        if page:
            try:
                for i in data['problemSet']:
                    question = models.Question.objects.filter(index=i['index'], page=page).first()
                    if question.need is False:
                        try:
                            pass
                        except Exception as e:
                            print('error2', e)
                    if question.type is True:
                        models.CAnswer.objects.create(question=question, option=i['option'], respondent=respondent)
                    else:
                        models.FAnswer.objects.create(question=question, answer=i['answer'], respondent=respondent)
                if page.isopen is not True:
                    item.status = True
                    item.nums += 1
                    item.save()
                else:
                    item.nums += 1
                    item.save()
                return JsonResponse({
                    'code': 0,
                    'message': 'Submit successfully'
                })
            except Exception as e:
                return JsonResponse({
                    'code': 7,
                    'message': str(e)
                })
        return JsonResponse({
            'code': 2,
            'message': 'Invalid sessionURl'
        })


class QuestionResult(ControlView, View):
    @staticmethod
    def get(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        pid = request.GET.get('id')
        try:
            result = dict()
            page = models.Page.objects.filter(user__token=token, id=pid).first()
            result['title'] = pid.title
            result['question'] = list()
            result['total'] = 0
            try:
                for i in models.Entrance.objects.filter(page=page):
                    page['total'] += i.nums
            except Exception as e:
                return JsonResponse({
                    'code': 0,
                    'message': str(e) + 'None U_P of this Page',
                    'data': {'title': 'None', 'total': 0, 'question': []}
                })
            for i in models.Question.objects.filter(page=page):
                question = {'title': i.title, 'type': i.type, 'index': i.index, 'option': {}, 'answer': {},
                            'total': None}
                if i.type is True:
                    question['total'] = models.CAnswer.objects.filter(question=i).count()
                    for ii in models.Choice.objects.filter(question=i):
                        question['option'][ii.text] = models.CAnswer.objects.filter(option=ii.option,
                                                                                    question=i).count()
                else:
                    question['total'] = models.FAnswer.objects.filter(question=i).count()
                    item = set()
                    for ii in models.FAnswer.objects.all():
                        item.add(ii.answer)
                    for ii in item:
                        question['answer'] = models.FAnswer.objects.filter(answer=ii, question=i).count()
                page['question'].append(question)
            return JsonResponse({
                'code': 0,
                'message': 'get it',
                'data': page
            })
        except Exception as e:
            return JsonResponse({
                'code': 7,
                'message': str(e)
            })

    @staticmethod
    def post(request, *args, **kwargs):
        return JsonResponse({
            'code': 0,
            'message': 'You can get result here'
        })
