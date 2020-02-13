from stark.service.v1 import StarkModelForm
from web import models


class PaymentRecordModelForm(StarkModelForm):
    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'note']
