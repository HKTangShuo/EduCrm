from stark.service.v1 import StarkHandler, get_choice_text
from stark.utils.resetpwd import ResetPasswordHandler
from web.modelforms.saler import SalerAddModelForm, SalerUpdateModelForm
from rbac.models import Role
from stark.service.base import PermissionHandler


class SalerHandler(PermissionHandler,ResetPasswordHandler, StarkHandler):
    list_display = ['nickname', 'phone', get_choice_text('性别', 'gender'), ResetPasswordHandler.display_reset_pwd]

    def get_model_form_class(self, is_add, request, *args, **kwargs):
        if is_add:
            return SalerAddModelForm

        return SalerUpdateModelForm

    def save(self, request, form, is_update, *args, **kwargs):
        if not is_update:
            form.save()
            role_obj = Role.objects.filter(title='销售').first()
            saler_obj = form.instance
            saler_obj.roles.add(role_obj)
            saler_obj.save()
        form.save()
