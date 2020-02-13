from stark.service.v1 import StarkHandler, get_choice_text
from django.urls import re_path
from web.modelforms.payment import PaymentRecordModelForm
from web.modelforms.student import StudentAddModelForm
from web import models
from django.shortcuts import HttpResponse
from stark.service.base import PermissionHandler


class PaymentRecordHandler(PermissionHandler,StarkHandler):
    list_display = ['consultant', get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 'apply_date',
                    get_choice_text('状态', 'confirm_status')]

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        customer_id = kwargs['customer_id']
        if models.Student.objects.filter(customer_id=customer_id):
            return self.model_form_class
        return StudentAddModelForm

    model_form_class = PaymentRecordModelForm

    def get_list_display(self, request, *args, **kwargs):
        return self.list_display

    def get_queryset(self, request, *args, **kwargs):
        current_user_id = request.session['user_id']
        return self.model_class.objects.filter(customer_id=kwargs['customer_id'],
                                               customer__consultant_id=current_user_id)

    def get_urls(self):
        patterns = [re_path(r'^list/(?P<customer_id>\d+)/$',
                            self.wrapper(self.changelist_view),
                            name=self.get_list_url_name),
                    re_path(r'^add/(?P<customer_id>\d+)/$',
                            self.wrapper(self.add_view),
                            name=self.get_add_url_name),
                    ]

        return patterns

    def save(self, request, form, is_update, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        obj_exists = models.Customer.objects.filter(id=customer_id, consultant_id=current_user_id).exists()
        if not obj_exists:
            return HttpResponse('呵呵！非法操作！')
        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_user_id
        form.save()
