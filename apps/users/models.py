# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default=u'female', max_length=10)
    address = models.CharField(max_length=11, default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username
