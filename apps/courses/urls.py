# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView

urlpatterns = [
    # 课程机构
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    # 课程详情信息(包括课程章节)
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_detail'),

]
