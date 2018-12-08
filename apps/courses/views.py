# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse

from .models import CoursesOrg
from organization.models import CityDict
from operation.models import UserFavorite, CourseComments
from courses.models import Courses, CoursesResource
from django.shortcuts import render
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import JsonResponse


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
        course = Courses.objects.get(id=course_id)

        # 增加点击数
        course.click_nums += 1
        course.save()

        # 收藏显示
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Courses.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', locals())


class CourseInfoView(View):
    """
    课程章节详情
    """

    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))
        all_resourse = CoursesResource.objects.filter(course=course)
        return render(request, 'course-video.html', locals())


class CourseCommentView(View):
    """
    课程评论
    """

    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.filter(course=course)

        # 用户课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有的课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的 用户 学过其他所有的课程
        relate_courses = Courses.objects.filter(id__in=course_id)

        return render(request, 'course-comment.html', locals())

    def post(self, request):
        pass


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comment = CourseComments()
            course = Courses.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return JsonResponse({'status': 'success', 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加失败'})
