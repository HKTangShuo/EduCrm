#根路由写法：
    # from django.contrib import admin
    # from django.urls import path,re_path,include
    # from stark.service.v1 import site
    # from web.views import account
    # urlpatterns = [
    #     path('admin/', admin.site.urls),
    #     re_path(r"stark/",site.urls),
    #     re_path(r"login/",account.login,name='login'),
    #     re_path(r'^rbac/', include(('rbac.urls','rbac'))),
    #     re_path(r'^index/',account.index,name='index')
    # ]


# 项目下创建stark.py
    # from stark.service.v1 import site
    # from web import models

    # from web.views.courserecord import CourseRecordHandler
    #
    # site.register(models.School,SchoolHandler)



#datetime picker:
    # from django import forms
    # from web.models import Repertory
    # from stark.forms.widgets import DateTimePickerInput
    # from stark.service.v1 import StarkModelForm
    #
    #
    # class RepertoryModelForm(StarkModelForm):
    #     class Meta:
    #         model = Repertory
    #         fields = '__all__'
    #         widgets = {
    #             'add_date': DateTimePickerInput,
    #             'product_date': DateTimePickerInput
    #         }


###############查看跟进记录#########################
"""
  def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '操作'
        tpl = '<a href="%s">编辑</a> <a href="%s">删除</a>' % (
            reverse('stark:web_providerrecord_change',
                    kwargs={'provider_id': kwargs['provider_id'], 'pk': obj.pk}),
            reverse('stark:web_providerrecord_delete',
                    kwargs={'provider_id': kwargs['provider_id'], 'pk': obj.pk}))
        return mark_safe(tpl)

"""
    # """
    #   patterns = [
    #             re_path(r'^list/(?P<provider_id>\d+)/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
    #             re_path(r'^add/(?P<provider_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
    #             re_path(r'^change/(?P<provider_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
    #                     name=self.get_change_url_name),
    #             re_path(r'^delete/(?P<provider_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
    #                     name=self.get_delete_url_name),
    #         ]
    # """