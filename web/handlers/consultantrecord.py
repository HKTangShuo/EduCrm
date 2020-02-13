from stark.service.v1 import StarkHandler
from django.urls import re_path
from web.modelforms.consultant import ConsultantModelForm
from django.utils.safestring import mark_safe

from stark.service.base import PermissionHandler

class ConsultantHandler(PermissionHandler,StarkHandler):
    list_display = ['customer', 'consultant', 'note', 'date']
    change_list_template = 'record_view.html'
    model_form_class = ConsultantModelForm

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "操作"
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            self.reverse_change_url(pk=obj.pk, cusotomer_id=kwargs['cusotomer_id']),
            self.reverse_delete_url(pk=obj.pk, cusotomer_id=kwargs['cusotomer_id']))
        return mark_safe(tpl)

    def get_queryset(self, request, *args, **kwargs):
        return self.model_class.objects.filter(customer_id=kwargs['cusotomer_id'], )

    def get_urls(self):
        patterns = [re_path(r'^list/(?P<cusotomer_id>\d+)/$',
                            self.wrapper(self.changelist_view),
                            name=self.get_list_url_name),
                    re_path(r'^add/(?P<cusotomer_id>\d+)/$',
                            self.wrapper(self.add_view),
                            name=self.get_add_url_name),
                    re_path(r'^change/(?P<cusotomer_id>\d+)/(?P<pk>\d+)/$',
                            self.wrapper(self.change_view),
                            name=self.get_change_url_name),
                    re_path(r'^delete/(?P<cusotomer_id>\d+)/(?P<pk>\d+)/$',
                            self.wrapper(self.delete_view),
                            name=self.get_delete_url_name),
                    ]

        return patterns

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            form.instance.customer_id = kwargs['cusotomer_id']
            form.instance.consultant_id = request.session['user_info']['id']
        form.save()
