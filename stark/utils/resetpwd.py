from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.urls import re_path
from web import models


class ResetPasswordHandler():
    # 用户重置密码功能
    # 继承  list_display =  [ResetPasswordHadnler.display_reset_pwd]
    def display_reset_pwd(self, obj=None, is_header=None):
        if is_header:
            return '重置密码'
        return mark_safe('<a href="%s">重置密码</a>' % self.reverse_reset_pwd_url(pk=obj.pk))

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
        patterns = [re_path(r'^reset/password/(?P<pk>\d+)/$',
                            self.wrapper(self.reset_pwd),
                            name=self.get_reset_pwd_url_name)
                    ]
        return patterns

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm

        return UserInfoUpdateModelForm


"""
Modelform 


class TeacherAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码', widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
                                       error_messages={'required': "确认密码不能为空！"})

    class Meta:
        model = models.Teacher
        fields = ['name', 'password', 'confirm_password',
                  'nickname', 'gender', 'wechat', 'phone',
                  'course', 'free_time']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_confirm_password(self):

        if self.cleaned_data.get('password') != self.cleaned_data['confirm_password']:
            raise ValidationError('两次密码不一致')
        return self.cleaned_data['confirm_password']

    def clean(self):
        if not self.cleaned_data.get('password'):
            raise ValidationError('请输入密码')
        raw_password = self.cleaned_data['password']
        self.cleaned_data['password'] = raw_password
        return self.cleaned_data


class TeacherUpdateModelForm(StarkModelForm):
    class Meta:
        model = models.Teacher
        fields = ['nickname', 'gender', 'phone', 'wechat', 'course', 'free_time']


"""
