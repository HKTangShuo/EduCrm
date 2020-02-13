from stark.service.v1 import StarkHandler, get_datetime_text, get_choice_text, get_m2m_text
from web import models
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.db import transaction
from django.shortcuts import HttpResponse
from django.shortcuts import reverse
from web.modelforms.customer import PublicCustomerModelForm, PrivateCustomerModelForm
from stark.service.base import PermissionHandler

class PublicCustomerHandler(PermissionHandler,StarkHandler):
    # 公户
    model_form_class = PublicCustomerModelForm

    def action_multi_apply(self, request, *args, **kwargs):
        """
          批量申请到私户
          :return:
          """
        # 客户id

        pk_list = request.POST.getlist('pk')
        # 更新到我的私户(consultant=当前自己的id)
        ######这里还要改

        current_user_id = request.session['user_info']['id']
        # 限制 如过大于150人 就不可以申请到私户
        private_customer_count = models.Customer.objects.filter(consultant__id=current_user_id, status=2).count()
        if (private_customer_count + len(pk_list)) > models.Customer.MAX_PRIVATE_COUNT:
            return HttpResponse(
                "私户中已有%s人,最多只可申请%s人" % (
                    private_customer_count, models.Customer.MAX_PRIVATE_COUNT - private_customer_count))
        flag = False
        with transaction.atomic():
            origin_queryset = models.Customer.objects.filter(pk__in=pk_list, status=2,
                                                             consultant__isnull=True).select_for_update()
            if not origin_queryset:
                return HttpResponse("获取用户失败或当前用户已报名，请申请其他用户")
            if len(origin_queryset) == len(pk_list):
                origin_queryset.update(consultant_id=current_user_id)
                flag = True
        if not flag:
            return HttpResponse("手速太慢，已有选中客户被其他人申请到私户，请重新申请")

    action_multi_apply.text = "批量申请到我的私户"
    action_list = [action_multi_apply]

    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "跟进记录"
        tpl = '<a href="%s" target="_blank">查看跟进记录</a>' % (
            self.reverse_record_view_url(pk=obj.pk))
        return mark_safe(tpl)

    list_display = [StarkHandler.display_checkbox, 'parent_name', 'wechat',
                    get_choice_text('来源', 'source'), get_m2m_text('咨询课程', 'course'),
                    'remark', get_datetime_text('咨询日期', 'date'), display_record
                    ]

    def get_queryset(self, request, *args, **kwargs):
        """加条件来显示的数据(filter)"""
        return self.model_class.objects.filter(consultant__isnull=True)

    def extra_urls(self):
        patterns = [url(r'^consultant/record/(?P<pk>\d+)/$',
                        self.wrapper(self.record_view),
                        name=self.get_record_view_url_name)
                    ]
        return patterns

    def reverse_record_view_url(self, *args, **kwargs):
        return self.reverse_commons_url(
            self.get_record_view_url_name, *args, **kwargs)

    @property
    def get_record_view_url_name(self):
        return self.get_url_name('consultant_record')

    def record_view(self, request, pk):
        msg = models.ConsultRecord.objects.filter(customer_id=pk)

        return render(request, 'consult_record.html', {'body_list': msg})


class PrivateCustomerHandler(PermissionHandler,StarkHandler):
    # 私户
    def display_pay(self, obj=None, is_header=None, *args, **kwargs):

        if is_header:
            return "缴费记录"
        tpl = mark_safe(
            '<a href="%s" target="_blank">查看缴费记录</a>' % reverse('stark:web_paymentrecord_list',
                                                                kwargs={'customer_id': obj.pk}))
        return tpl

    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "跟进记录"

        tpl = mark_safe(
            '<a href="%s" target="_blank">查看跟进记录</a>' % reverse('stark:web_consultrecord_list',
                                                                kwargs={'cusotomer_id': obj.pk}))
        return tpl

    def action_multi_to_pub(self, request, *args, **kwargs):
        """
        批量删除（如果想要定制执行成功后的返回值，那么就为action函数设置返回值即可。）
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, consultant_id=current_user_id).update(consultant_id='')

    action_list = [action_multi_to_pub]
    action_multi_to_pub.text = "批量移除到公户"
    model_form_class = PrivateCustomerModelForm
    list_display = [
        StarkHandler.display_checkbox,
        'parent_name',
        'wechat',
        get_m2m_text('咨询的课程', 'course'), get_choice_text(
            '状态',
            'status'), display_pay, display_record
    ]

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            form.instance.consultant_id = request.session['user_info']['id']
            form.save()
        form.save()
