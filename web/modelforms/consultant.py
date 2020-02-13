from web import models
from stark.service.v1 import StarkModelForm


class ConsultantModelForm(StarkModelForm):
    class Meta:
        model = models.ConsultRecord
        exclude = ['consultant', 'customer']
