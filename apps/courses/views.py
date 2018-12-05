# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from .models import CoursesOrg
from organization.models import CityDict
from operation.models import UserFavorite
from courses.models import Courses
from django.shortcuts import render


class CourseListView(View):
    def get(self, request):
        # 热门课程推荐
        hot_courses = Courses.objects.all().order_by('-click_nums')[:3]

        page = request.GET.get('page', 1)
        sort = request.GET.get('sort', '')
        if sort == 'students':
            order_param = '-students'
        elif sort == 'hot':
            order_param = '-hot'
        else:
            order_param = '-id'

        all_courses = Courses.objects.all().order_by(order_param)

        # 第二个参数表示每页设置2页
        paginator = Paginator(all_courses, 9)

        current_page = int(page) if page else ''

        try:
            all_courses = paginator.page(page)
        except PageNotAnInteger:
            all_courses = paginator.page(1)
        except EmptyPage:
            all_courses = paginator.page(paginator.num_pages)

        return render(request, 'course-list.html', locals())


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Courses.objects.filter(id=course_id)
        print course
        return render(request, 'course-detail.html', locals())
