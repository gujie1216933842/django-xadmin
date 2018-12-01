# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from .models import CoursesOrg

from operation.models import UserFavorite
from courses.models import Courses
from django.shortcuts import render


class CourseListView(View):
    def get(self, request):
        all_courses = Courses.objects.all()

        return render(request, 'course-list.html', locals())
