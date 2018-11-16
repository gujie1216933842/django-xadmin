# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import EmailVerifyRecode, UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        """
        自定义登录,自己的后台逻辑
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def index(request):
    EmailVerifyRecode.objects.filter()


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username, password)
        if user is not None:
            login(request, user)
            return render(request, "index.html", locals())
        else:
            return render(request, 'login.html', locals())

    return render(request, 'login.html', locals())
