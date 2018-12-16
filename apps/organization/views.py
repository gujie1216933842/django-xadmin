# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from .models import CoursesOrg, CityDict, Teacher
from .forms import UserAskForm
from operation.models import UserFavorite
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

        has_fav = False
        if request.user.is_authenticated():
            # 判断用户登录状态
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', locals())


class OrgCourserView(View):
    """
    机构课程列表页
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_courses = course_org.courses_set.all()

        has_fav = False
        if request.user.is_authenticated():
            # 判断用户登录状态
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', locals())


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CoursesOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            # 判断用户登录状态
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', locals())


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CoursesOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated():
            # 判断用户登录状态
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', locals())


class AddFavView(View):
    """
    用户收藏,用户取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            exist_records.delete()
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return JsonResponse({'status': 'success', 'msg': '已收藏'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    """
    讲师列表页
    """

    def get(self, request):
        all_teachers = Teacher.objects.all()

        sorted_teachers = all_teachers.order_by('-click_nums')[:3]  # 列出点击量最高的3个讲师

        return render(request, 'teachers-list.html', locals())


class TeacherDetailView(View):
    """
    讲师详情页
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        all_courses = Courses.objects.filter(teacher=teacher)

        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:3]  # 列出点击量最高的3个讲师

        return render(request, 'teacher-detail.html', locals())
