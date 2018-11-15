# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import EmailVerifyRecode
from django.shortcuts import render


# Create your views here.

def index(request):
    EmailVerifyRecode.objects.filter()
