# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程机构
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

]
