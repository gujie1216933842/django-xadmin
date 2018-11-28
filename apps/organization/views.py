# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from .models import CoursesOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CoursesOrg.objects.all()  #
        org_nums = all_orgs.count()

        all_citys = CityDict.objects.all()  # 所有城市

        # 取出帅选城市
        city_id = request.GET.get('city', '')
        if city_id:
            print(city_id)
            all_orgs = CoursesOrg.objects.filter(city_id=city_id)
            print(all_orgs)

        # 对课程机构进行分页, 第二个参数表示每页设置2页
        paginator = Paginator(all_orgs, 2)

        page = request.GET.get('page', 1)
        currentPage = int(page)
        try:
            all_orgs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_orgs = paginator.page(1)
        except EmptyPage:
            all_orgs = paginator.page(paginator.num_pages)

        return render(request, 'org-list.html', locals())
