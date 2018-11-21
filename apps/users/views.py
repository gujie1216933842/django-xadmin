# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import EmailVerifyRecode, UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email


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


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request, user)
                return render(request, "index.html", locals())
            else:
                return render(request, 'login.html', {'msg': '用户名或密码不正确'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            # 判断用户是否已经存在
            if UserProfile.objects.filter(email=username):
                msg = '用户已经存在'
                return render(request, 'register.html', locals())

            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')


class ActiveUserView(View):
    def get(self, request, active_code):
        rows_record = EmailVerifyRecode.objects.filter(code=active_code)
        if rows_record:
            for row_record in rows_record:
                email = row_record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        register_form = ForgetForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')

            send_register_email(email, 'forget')
            return render(request, 'send_success.html', locals())
        else:
            return render(request, 'forgetpwd.html', locals())


class ResetView(View):
    def get(self, request, active_code):
        rows_record = EmailVerifyRecode.objects.filter(code=active_code)
        if rows_record:
            for row_record in rows_record:
                email = row_record.email
                return render(request, 'password_reset.html', locals())
        else:
            return render(request, 'active_fail.html')
        return render(request, 'active_success.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                msg = '密码不一致!'
                return render(request, 'password_reset.html', locals())
            # 密码一致,进入密码修改流程
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            # 密码修改成功 ,返回 登录页面
            return render(request, 'login.html', locals())
        else:
            return render(request, '', locals())
