from stark.service.v1 import StarkHandler, get_choice_text, Option
from web import models
from web.modelforms.userinfo import UserinfoModelForm, UserInfoAddModelForm, UserInfoUpdateModelForm

from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from stark.service.base import PermissionHandler


class UserinfoHandler(PermissionHandler,StarkHandler):

    def display_reset_pwd(self, obj=None, is_header=None):
        if is_header:
            return '重置密码'
        return mark_safe('<a href="%s">重置密码</a>' % self.reverse_reset_pwd_url(pk=obj.pk))

    search_group = [
        Option(field='gender'),
    ]
    search_list = ['nickname__contains', 'name__contains']
    list_display = ['nickname', get_choice_text('性别', 'gender'), 'phone', 'email', 'depart', display_reset_pwd]

    def reset_pwd(self, request, pk):
        if request.method == 'GET':
            return render(request, 'stark/delete.html', {'msg': '重置密码', 'cancel': self.reverse_list_url()})
        user_obj = models.UserInfo.objects.filter(id=pk).first()
        if not user_obj:
            return HttpResponse('用户不存在')
        user_obj.password = '000000'
        user_obj.save()
        return redirect(self.reverse_list_url())

    def reverse_reset_pwd_url(self, *args, **kwargs):
        return self.reverse_commons_url(self.get_reset_pwd_url_name, *args, **kwargs)

    @property
    def get_reset_pwd_url_name(self):
        return self.get_url_name('reset_pwd')

    def extra_urls(self):
        patterns = [url(r'^reset/password/(?P<pk>\d+)/$',
                        self.wrapper(self.reset_pwd),
                        name=self.get_reset_pwd_url_name)
                    ]
        return patterns

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm

        return UserInfoUpdateModelForm
