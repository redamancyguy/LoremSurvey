from django.db import models
from pymongo import MongoClient

from user.models import User


class Respondent(models.Model):
    sid = models.BigIntegerField()
    name = models.CharField(max_length=32)
    school = models.CharField(max_length=32)
    major = models.CharField(max_length=32)
    Class = models.CharField(max_length=32)
    sex = models.CharField(max_length=8)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ("sid", "user")


class Page(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128)
    desc = models.TextField(max_length=1024, blank=True, null=True)
    emailTemplate = models.CharField(max_length=128, blank=True, null=True)
    startTime = models.DateTimeField('startTime', blank=True, null=True)
    stopTime = models.DateTimeField('stopTime', blank=True, null=True)
    open = models.BooleanField(default=False)
    running = models.BooleanField(default=False)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.BooleanField()
    index = models.IntegerField()
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128, default=None, blank=True, null=True)
    need = models.BooleanField(default=False)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)


class Choice(models.Model):  # 问题答案
    id = models.BigAutoField(primary_key=True)
    option = models.CharField(max_length=8, default=None)  # A B C D
    text = models.CharField(max_length=128, default=None)
    score = models.IntegerField(default=1)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)


class CAnswer(models.Model):  # 问卷结果
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None)
    option = models.CharField(max_length=8, default=None)
    respondent = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None, null=True, blank=True)


class FAnswer(models.Model):  # 问卷结果
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, default=None)
    answer = models.TextField(max_length=1024, default=None)
    respondent = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None, null=True, blank=True)


class Entrance(models.Model):
    id = models.BigAutoField(primary_key=True)
    page = models.ForeignKey('Page', on_delete=models.CASCADE, default=None)
    respondent = models.ForeignKey('Respondent', on_delete=models.CASCADE, default=None, null=True, blank=True)
    sessionUrl = models.UUIDField(max_length=128, default=None)
    status = models.BooleanField(default=False)
    nums = models.IntegerField(default=0)

    class Meta:
        unique_together = ('page', 'respondent')


class Mongo:
    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.client = MongoClient('39.104.209.232', 27017)

    def getClient(self):
        return self.client

    def close(self):
        self.client.close()
