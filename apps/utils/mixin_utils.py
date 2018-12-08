# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispath(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispath(request, *args, **kwargs)
