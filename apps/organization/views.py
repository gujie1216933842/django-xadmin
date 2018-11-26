# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import CoursesOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CoursesOrg.objects.all()  #
        org_nums = all_orgs.count()

        all_citys = CityDict.objects.all()  # 所有城市

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        print(p)
        orgs = p.page(page)
        print(orgs)

        return render(request, 'org-list.html',locals())
