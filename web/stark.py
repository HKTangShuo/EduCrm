from stark.service.v1 import site
from web import models

from web.handlers.student import StudentHandler
from web.handlers.teacher import TeacherHandler
from web.handlers.course import CoursetHandler
from web.handlers.saler import SalerHandler
from web.handlers.customer import PublicCustomerHandler
from web.handlers.customer import PrivateCustomerHandler
from web.handlers.consultantrecord import ConsultantHandler
from web.handlers.payment import PaymentRecordHandler
from web.handlers.checkpayment import CheckPaymentRecordHandler
from web.handlers.student import TeaStudentHandler
from web.handlers.courserecord import CourseRecordHandler
from web.handlers.checkcourserecord import CheckCourseRecordHandler
from web.handlers.courserecord import StuCourseRecordHandler

site.register(models.Teacher, TeacherHandler)
site.register(models.Student, StudentHandler)
site.register(models.Saler, SalerHandler)
site.register(models.Course, CoursetHandler)

site.register(models.Customer, PublicCustomerHandler, prev='pub')
site.register(models.Customer, PrivateCustomerHandler, prev='pri')
site.register(models.ConsultRecord, ConsultantHandler)  # 私户跟进记录增删改查
site.register(models.PaymentRecord, PaymentRecordHandler)  # 缴费记录
site.register(
    models.PaymentRecord,
    CheckPaymentRecordHandler,
    prev='check')  # 审核缴费
site.register(models.CourseRecord, CheckCourseRecordHandler, prev='check')
site.register(models.Student, TeaStudentHandler, prev='mystu')
site.register(models.CourseRecord, CourseRecordHandler)
site.register(models.CourseRecord, StuCourseRecordHandler, prev='stu')
