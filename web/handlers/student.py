from stark.service.v1 import StarkHandler, get_choice_text, get_m2m_text, Option
from web.modelforms.student import StudentAddModelForm, StudentUpdateModelForm
from stark.utils.resetpwd import ResetPasswordHandler
from django.urls import re_path
from django.utils.safestring import mark_safe
from web import models
from django.shortcuts import reverse
from rbac.models import Role
from stark.service.base import PermissionHandler


class StudentHandler(PermissionHandler, ResetPasswordHandler, StarkHandler):
    search_group = [
        Option(field='education'),
        Option(field='course'),
    ]
    search_list = ['stu_name__contains', 'teacher__nickname__contains']
    list_display = ['stu_name',
                    get_choice_text('性别', 'stu_gender'),
                    'school',
                    get_choice_text('年级', 'education'),
                    get_m2m_text('报名科目', 'course'),
                    get_m2m_text('任课老师', 'teacher'), ResetPasswordHandler.display_reset_pwd
                    ]

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        if is_add:
            return StudentAddModelForm

        return StudentUpdateModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        # 给学生分配教师的角色
        if not is_update:
            form.save()
            role_obj = Role.objects.filter(title='学生').first()
            student_obj = form.instance
            student_obj.roles.add(role_obj)
            student_obj.save()
        form.save()


#
# class StudentTeacherHadnler(StarkHandler):
#     # 老师查看自己的所有学生  点击操作某学生的上课记录
#     has_add_btn = False
#     search_list = ['stu_name__contains', ]
#
#     def display_record(self, obj=None, is_header=None, *args, **kwargs):
#         if is_header:
#             return "上课记录"
#         return mark_safe(
#             '<a href="%s" target="_blank">查看或添加上课记录</a>' % reverse('stark:web_courserecord_list',
#                                                                    kwargs={'teacher_id': kwargs['teacher_id'],
#                                                                            'student_id': obj.pk}))
#
#     list_display = ['stu_name',
#                     get_choice_text('性别', 'sex'),
#                     'school',
#                     get_choice_text('年级', 'education'),
#                     get_m2m_text('报名科目', 'course'), display_record
#                     ]
#
#     def get_urls(self):
#         patterns = [
#             re_path(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
#         ]
#         return patterns
#
#     def get_queryset(self, request, *args, **kwargs):
#         if int(request.session['user_id']) != int(kwargs['teacher_id']):
#             return False
#
#         teacher_obj = models.Teacher.objects.filter(id=kwargs['teacher_id']).first()
#         return teacher_obj.student_set.all()


class TeaStudentHandler(PermissionHandler, StarkHandler):
    # 老师 查看自己的学生
    search_list = ['stu_name__contains']

    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "课堂反馈"
        return mark_safe(
            '<a href="%s" target="_blank">查看课堂反馈</a>' % reverse('stark:web_courserecord_list',
                                                                kwargs={'student_id': obj.pk}))

    list_display = ['stu_name', get_choice_text('性别', 'stu_gender'), 'school', get_choice_text('年级', 'education'),
                    display_course_record]
    has_add_btn = False

    def get_list_display(self, request, *args, **kwargs):
        return self.list_display

    def get_urls(self):
        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
        ]
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_id']
        teach_obj = models.Teacher.objects.filter(id=current_user_id).first()

        return self.model_class.objects.filter(teacher=teach_obj, teacher__isnull=False)
