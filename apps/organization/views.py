# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from .models import CoursesOrg, CityDict
from .forms import UserAskForm
from courses.models import Courses


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_orgs = CoursesOrg.objects.all()
        all_citys = CityDict.objects.all()  # 所有城市

        page = request.GET.get('page', 1)
        # 取出帅选城市
        city_id = request.GET.get('city', '')
        # 取机构类别
        category = request.GET.get('ct', '')
        params = {}
        if city_id:
            params = {
                'city_id': city_id
            }

        if category:
            params = {
                'category': category
            }
        if city_id and category:
            params = {
                'city_id': city_id,
                'category': category
            }

        sort = request.GET.get('sort', '')
        if sort == 'students':
            order_param = '-students'
        elif sort == 'courses':
            order_param = '-course_nums'
        else:
            order_param = '-id'

        all_orgs = CoursesOrg.objects.filter(**params).order_by(order_param)
        org_nums = all_orgs.count()  # 筛选条件下的机构总数量

        # 第二个参数表示每页设置2页
        paginator = Paginator(all_orgs, 2)

        current_city_id = int(city_id) if city_id else ''
        current_page = int(page) if page else ''

        try:
            all_orgs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_orgs = paginator.page(1)
        except EmptyPage:
            all_orgs = paginator.page(paginator.num_pages)

        return render(request, 'org-list.html', locals())


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(request.POST)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': userask_form.errors})


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', locals())


class OrgCourserView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.all()
        return render(request, 'org-detail-course.html', locals())


