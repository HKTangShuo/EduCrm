from stark.service.v1 import StarkModelForm
from web import models


class PublicCustomerModelForm(StarkModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant',
                   'status',
                   ]


class PrivateCustomerModelForm(StarkModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant', 'status']
