from stark.service.v1 import StarkHandler, get_choice_text, Option
from django.urls import re_path
from django.conf import settings
from stark.service.base import PermissionHandler


class CheckPaymentRecordHandler(PermissionHandler,StarkHandler):
    search_group = [Option('confirm_status'), Option('consultant')]
    order_list = ['confirm_status']
    list_display = [StarkHandler.display_checkbox, 'consultant', 'customer', 'paid_fee',
                    get_choice_text('类型', 'pay_type'),
                    get_choice_text('状态', 'confirm_status'), 'apply_date']

    def get_list_display(self, request, *args, **kwargs):
        return self.list_display

    has_add_btn = False

    def get_urls(self):
        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist_view), name=self.get_list_url_name),
        ]
        return patterns

    def action_multi_check(self, request, *args, **kwargs):
        pk_list = request.POST.getlist('pk')
        for pk in pk_list:
            payrecord_obj = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payrecord_obj:
                continue
            payrecord_obj.confirm_status = 2
            payrecord_obj.customer.status = 1
            payrecord_obj.save()
            payrecord_obj.customer.save()

    action_multi_check.text = "批量通过审核"

    def action_multi_cancle(self, request, *args, **kwargs):

        pk_list = request.POST.getlist('pk')
        for pk in pk_list:
            payrecord_obj = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payrecord_obj:
                continue
            payrecord_obj.confirm_status = 3
            payrecord_obj.save()

    action_multi_cancle.text = "批量驳回"

    action_list = [action_multi_check, action_multi_cancle]
