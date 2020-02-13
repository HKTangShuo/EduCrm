from django.db import models
from rbac.models import UserInfo as RbacModel
from django.conf import settings


# Create your models here.
class UserInfo(RbacModel):
    nickname = models.CharField(verbose_name='姓名', max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=32)
    gender_choices = (
        (1, "男"),
        (2, '女')
    )
    gender = models.IntegerField(
        verbose_name="性别",
        choices=gender_choices,
        default=1)

    def __str__(self):
        return '%s' % self.nickname


class Course(models.Model):
    name = models.CharField(verbose_name='课程名称', max_length=32)

    def __str__(self):
        return self.name


class Customer(models.Model):
    MAX_PRIVATE_COUNT = 20
    parent_name = models.CharField(verbose_name='家长姓名', max_length=16)
    wechat = models.CharField(
        verbose_name="联系方式",
        max_length=64,
        unique=True,
        help_text="QQ/微信/电话")

    source_choice = [
        (1, '广告'),
        (2, '学员介绍'),
        (3, '微信好友'),
        (4, '其他'),
    ]
    source = models.SmallIntegerField(
        verbose_name='来源', choices=source_choice, default=1)
    course = models.ManyToManyField(verbose_name='咨询课程', to='Course')
    consultant = models.ForeignKey(
        verbose_name='课程顾问',
        to='Saler',
        related_name='consultant',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    status_choices = [
        (settings.STATUS_PAYED, '已缴费'),
        (settings.STATUS_UNPAYED, '未缴费'),
        (settings.STATUS_OWN, '欠费'),
    ]
    status = models.IntegerField(
        verbose_name='状态',
        choices=status_choices,
        default=2,
        help_text='学生是否报名')
    remark = models.TextField(verbose_name='学生简略信息', max_length=248)
    date = models.DateField(verbose_name="咨询日期", auto_now_add=True)

    def __str__(self):
        return '学生家长：%s' % self.parent_name


class ConsultRecord(models.Model):
    customer = models.ForeignKey(
        to=Customer,
        verbose_name="跟进的客户",
        on_delete=models.CASCADE)
    consultant = models.ForeignKey(
        verbose_name="跟踪人",
        to='UserInfo',
        on_delete=models.CASCADE)
    note = models.TextField(verbose_name='跟进内容', max_length=500)
    date = models.DateField(verbose_name='跟进日期', auto_now_add=True)


class Teacher(UserInfo):
    wechat = models.CharField(verbose_name='微信', max_length=32)
    course = models.ManyToManyField(to='Course', verbose_name='科目')
    free_time = models.CharField(verbose_name='空余时间', max_length=128)

    def __str__(self):
        return '%s' % self.nickname


class Student(UserInfo):
    customer = models.ForeignKey(
        verbose_name='客户信息',
        to='Customer',
        on_delete=models.CASCADE, null=True, blank=True)
    stu_name = models.CharField(verbose_name='学生姓名', max_length=32)
    gender_choice = ((1, '男'), (2, '女'))
    stu_gender = models.IntegerField(verbose_name='性别', choices=gender_choice)
    education_choice = [
        (1, '小学'),
        (2, '初中'),
        (3, '高中'),
    ]
    education = models.IntegerField(
        verbose_name='年级',
        choices=education_choice,
        blank=True,
        null=True)
    school = models.CharField(
        verbose_name="学校",
        max_length=64,
        blank=True,
        null=True)
    course = models.ManyToManyField(to='Course', verbose_name='课程')
    teacher = models.ManyToManyField(to='Teacher', verbose_name='任课老师', null=True, blank=True)

    def __str__(self):
        return self.stu_name


class CourseRecord(models.Model):
    student = models.ForeignKey(
        verbose_name="学生姓名",
        to='Student',
        on_delete=models.CASCADE)
    course = models.ForeignKey(to='Course', verbose_name='科目', on_delete=models.CASCADE)
    record_num = models.PositiveIntegerField(verbose_name="节次")
    teacher = models.ForeignKey(
        verbose_name='讲师',
        to='Teacher',
        on_delete=models.CASCADE)
    date = models.DateField(verbose_name="上课日期", )

    knowledge_points = models.TextField(verbose_name='授课知识点')
    execption = models.TextField(verbose_name='下节课展望或作业')
    status_choice = (
        (settings.RECORD_CHECKED, '已审核'), (settings.RECORD_UNCHECKED, '未审核'), (settings.RECORD_REFUSED, '已驳回'))
    status = models.IntegerField(choices=status_choice, default=2, verbose_name='状态')

    def __str__(self):
        return "%s %s" % (self.teacher, self.record_num)


class Saler(UserInfo):
    pass


class PaymentRecord(models.Model):
    customer = models.ForeignKey(
        Customer,
        verbose_name="客户",
        on_delete=models.CASCADE)
    consultant = models.ForeignKey(
        verbose_name="课程顾问",
        to='Saler',
        help_text="谁签的单就选谁",
        on_delete=models.CASCADE)
    pay_type_type = ((1, '学费'), (2, '试听'), (3, '退费'), (4, '其他'))
    pay_type = models.IntegerField(verbose_name='缴费类型', default=1, choices=pay_type_type)
    paid_fee = models.IntegerField(verbose_name="金额", default=0)
    apply_date = models.DateTimeField(verbose_name="申请日期", auto_now_add=True)

    confirm_status_choices = (
        (1, '申请中'),
        (2, '已确认'),
        (3, '已驳回'),
    )
    confirm_status = models.IntegerField(
        verbose_name="确认状态",
        choices=confirm_status_choices,
        default=1)
    confirm_date = models.DateTimeField(
        verbose_name="确认日期", null=True, blank=True)
    confirm_user = models.ForeignKey(
        verbose_name="审批人",
        to='UserInfo',
        related_name='confirms',
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    note = models.TextField(verbose_name="备注", blank=True, null=True)
