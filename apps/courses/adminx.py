# -*- coding: utf-8 -*-
import xadmin
from .models import Courses, Lesson, Vedio, CoursesResource


class CoursesAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                    'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',
                   'add_time']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CoursesResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Courses, CoursesAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Vedio, VedioAdmin)
xadmin.site.register(CoursesResource, CoursesResourceAdmin)
