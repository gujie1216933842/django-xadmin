# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView,VedioPlayView

urlpatterns = [
    # 课程机构
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程详情信息(包括课程章节)
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),

    # 添加课程评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

    # 访问的视频地址
    url(r'^vedio/(?P<vedio_id>\d+)/$', VedioPlayView.as_view(), name='vedio_play'),

]
