from django.db import models
from django.utils import timezone

class User(models.Model):
    sid = models.BigIntegerField()
    name = models.CharField(max_length=32)
    school = models.CharField(max_length=32)
    major = models.CharField(max_length=32)
    classn = models.CharField(max_length=32)
    sex = models.CharField(max_length=8)
    phone = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    muid = models.BigIntegerField(default=None)
    class Meta:
        unique_together = ("sid", "muid")


class Page(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128, default=None)
    desc = models.CharField(max_length=128, default=None)
    stime = models.DateTimeField('startTime', default=None)
    etime = models.DateTimeField('startTime', default=None)
    isopen = models.CharField(max_length=8, default=None)
    muid = models.BigIntegerField(default=None)


class Cquestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.IntegerField(default=None)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    need = models.CharField(max_length=8)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE)


class Choice(models.Model):  # 问题答案
    id = models.BigAutoField(primary_key=True)
    option = models.CharField(max_length=8)  # A B C D
    text = models.CharField(max_length=128, default=None)
    score = models.IntegerField(default=1)
    cqid = models.ForeignKey('Cquestion', on_delete=models.CASCADE)


class Fquestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    index = models.IntegerField(default=None)
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    need = models.CharField(max_length=8)
    exampleAnswer = models.TextField(max_length=1024)
    score = models.IntegerField(default=1)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE)


class Canswer(models.Model):  # 问卷结果
    id = models.BigAutoField(primary_key=True)
    cqid = models.ForeignKey('Cquestion', on_delete=models.CASCADE)
    option = models.CharField(max_length=8)  # A B C D
    uid = models.ForeignKey('User', on_delete=models.CASCADE,default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE,default=None)


class Fanswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    fqid = models.ForeignKey('Fquestion', on_delete=models.CASCADE)
    answer = models.TextField(max_length=1024)
    uid = models.ForeignKey('User', on_delete=models.CASCADE,default=None)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE,default=None)


class U_P(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=4)
    pid = models.ForeignKey('Page', on_delete=models.CASCADE)
    uid = models.ForeignKey('User', on_delete=models.CASCADE)
    sessionid = models.UUIDField(max_length=64, default=None)
    muid = models.BigIntegerField(default=None)
    class Meta:
        unique_together = ("pid", "uid")



