from stark.service.v1 import StarkHandler, get_choice_text, Option
from django.urls import re_path
from django.conf import settings
from django.utils.safestring import mark_safe
from web import models
from django.shortcuts import render
from stark.service.base import PermissionHandler

class CheckCourseRecordHandler(PermissionHandler,StarkHandler):
    # 审核查看页面
    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'

        tpl = '<a href="%s" target="_blank">反馈详细信息</a>' % self.reverse_record_detail_url(
            pk=obj.pk)
        return mark_safe(tpl)

    search_group = [Option('status'), Option('teacher')]
    order_list = ['-status']
    list_display = [
        StarkHandler.display_checkbox,
        'teacher',
        'student',
        'course',
        'record_num',
        'date',
        get_choice_text(
            '状态',
            'status'),
        display_edit_del]

    def get_list_display(self, request, *args, **kwargs):
        return self.list_display

    has_add_btn = False

    @property
    def get_record_detail_url_name(self):
        return self.get_url_name('record_detail')

    def get_urls(self):
        patterns = [
            re_path(
                r'^list/$',
                self.wrapper(
                    self.changelist_view),
                name=self.get_list_url_name),
            re_path(
                r'^list/(?P<pk>\d+)/$',
                self.wrapper(
                    self.record_detail),
                name=self.get_record_detail_url_name),
        ]
        return patterns

    def reverse_record_detail_url(self, *args, **kwargs):
        return self.reverse_commons_url(
            self.get_record_detail_url_name, *args, **kwargs)

    def record_detail(self, request, pk):
        record = models.CourseRecord.objects.filter(id=pk).first()
        return render(request, 'course_record.html', {'record': record})

    def action_multi_check(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('pk')
        for pk in pk_list:
            course_record_obj = self.model_class.objects.filter(
                id=pk, status=settings.RECORD_UNCHECKED).first()
            if not course_record_obj:
                continue
            course_record_obj.status = settings.RECORD_CHECKED
            course_record_obj.save()

    action_multi_check.text = "批量通过审核"

    def action_multi_cancle(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('pk')
        for pk in pk_list:
            course_record_obj = self.model_class.objects.filter(
                id=pk, status=settings.RECORD_UNCHECKED).first()
            if not course_record_obj:
                continue
            course_record_obj.status = settings.RECORD_REFUSED
            course_record_obj.save()

    action_multi_cancle.text = "批量驳回"

    action_list = [action_multi_check, action_multi_cancle]
