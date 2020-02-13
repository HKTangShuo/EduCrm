from stark.service.v1 import StarkModelForm
from web import models

from stark.forms.widgets import DateTimePickerInput


class CourseRecordModelForm(StarkModelForm):
    class Meta:
        model = models.CourseRecord
        fields = [
            'course',
            'record_num',
            'date',
            'knowledge_points',
            'execption']
        widgets = {
            'date': DateTimePickerInput,
        }
