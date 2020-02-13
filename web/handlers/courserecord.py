from stark.service.v1 import StarkHandler, get_datetime_text, get_choice_text, Option
from django.urls import re_path
from web.modelforms.courserecord import CourseRecordModelForm
from django.conf import settings
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse
from web import models
from django.shortcuts import render
from stark.service.base import PermissionHandler


class CourseRecordHandler(PermissionHandler, StarkHandler):
    # 老师查看或添加自己某个学生所有的课堂反馈
    search_group = [Option('status')]
    model_form_class = CourseRecordModelForm
    list_display = [
        'student', 'course', 'record_num', get_datetime_text(
            '上课时间', 'date'), get_choice_text(
            '状态', 'status')]

    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义页面显示的列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "编辑"
        return mark_safe(
            '<a href="%s">编辑</a>' %
            self.reverse_change_url(
                pk=obj.pk,student_id=kwargs['student_id']))
    def get_urls(self):
        patterns = [
            re_path(
                r'^list/(?P<student_id>\d+)$',
                self.wrapper(
                    self.changelist_view),
                name=self.get_list_url_name),
            re_path(
                r'^add/(?P<student_id>\d+)$',
                self.wrapper(
                    self.add_view),
                name=self.get_add_url_name),
            re_path(
                r'^change/(?P<student_id>\d+)/(?P<pk>\d+)/$',
                self.wrapper(
                    self.change_view),
                name=self.get_change_url_name),
        ]

        return patterns

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'

        tpl = '<a href="%s">反馈详细信息</a>' % (self.reverse_change_url(
            pk=obj.pk, student_id=kwargs['student_id']))
        return mark_safe(tpl)

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(student_id=kwargs['student_id'])

    def save(self, request, form, is_update, *args, **kwargs):
        if form.instance.status == settings.RECORD_CHECKED:
            return HttpResponse("已审核过的课堂反馈不可以被修改！")
        if is_update:
            form.instance.status = settings.RECORD_UNCHECKED

        form.instance.student_id = kwargs['student_id']
        form.instance.teacher_id = request.session['user_id']
        form.save()


class StuCourseRecordHandler(PermissionHandler, StarkHandler):
    # 学生查看自己的课堂反馈
    has_add_btn = False
    search_list = ['course__name__contains', 'teacher__nickname__contains']

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'

        tpl = '<a href="%s" target="_blank">反馈详细信息</a>' % self.reverse_record_detail_url(
            pk=obj.pk)
        return mark_safe(tpl)

    list_display = [
        'teacher', 'course', 'record_num', get_datetime_text(
            '上课时间', 'date')
    ]

    def get_urls(self):
        patterns = [re_path(r'^list/$',
                            self.wrapper(self.changelist_view),
                            name=self.get_list_url_name),
                    re_path(
                        r'^list/(?P<pk>\d+)/$',
                        self.wrapper(
                            self.record_detail),
                        name=self.get_record_detail_url_name),
                    ]
        return patterns

    @property
    def get_record_detail_url_name(self):
        return self.get_url_name('stu_record_detail')

    def reverse_record_detail_url(self, *args, **kwargs):
        return self.reverse_commons_url(
            self.get_record_detail_url_name, *args, **kwargs)

    def record_detail(self, request, pk):
        record = models.CourseRecord.objects.filter(id=pk).first()
        return render(request, 'course_record.html', {'record': record})

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_id']
        return self.model_class.objects.filter(student_id=current_user_id, status=settings.RECORD_CHECKED)
