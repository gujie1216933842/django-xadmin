# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import CoursesOrg, CityDict


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CoursesOrg.objects.all()  # 所有机构
        all_citys = CityDict.objects.all()  # 所有城市



        return render(request, 'org-list.html', locals())
