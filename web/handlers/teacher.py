from stark.service.v1 import StarkHandler, get_m2m_text, Option, get_choice_text
from web.modelforms.teacher import TeacherAddModelForm, TeacherUpdateModelForm
from stark.utils.resetpwd import ResetPasswordHandler
from rbac.models import Role
from stark.service.base import PermissionHandler


class TeacherHandler(PermissionHandler,ResetPasswordHandler, StarkHandler):
    list_display = ['nickname',
                    get_choice_text('性别', 'gender'),
                    'phone', 'wechat',
                    get_m2m_text('教授科目', 'course'), 'free_time', ResetPasswordHandler.display_reset_pwd]
    search_list = ['nickname__contains', 'free_time__contains']
    search_group = [
        Option(field='gender'),
        Option(field='course'),
    ]

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        if is_add:
            return TeacherAddModelForm

        return TeacherUpdateModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        # 给老师分配教师的角色
        if not is_update:
            form.save()
            role_obj = Role.objects.filter(title='教师').first()
            teacher_obj = form.instance
            teacher_obj.roles.add(role_obj)
        form.save()
