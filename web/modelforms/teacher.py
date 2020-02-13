from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from stark.service.v1 import StarkModelForm
from web import models


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
