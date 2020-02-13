from stark.service.v1 import StarkHandler
from stark.service.base import PermissionHandler


class CoursetHandler(PermissionHandler,StarkHandler):
    list_display = ['name', ]
