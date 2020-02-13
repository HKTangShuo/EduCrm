# Generated by Django 3.0.3 on 2020-02-12 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='课程名称')),
            ],
        ),
        migrations.CreateModel(
            name='Depart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='部门名称')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='账号')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.CharField(max_length=32, verbose_name='邮箱')),
                ('nickname', models.CharField(max_length=32, verbose_name='姓名')),
                ('phone', models.CharField(max_length=32, verbose_name='手机号')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女')], default=1, verbose_name='性别')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Depart', verbose_name='部门')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.Role', verbose_name='拥有的所有角色')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(max_length=16, verbose_name='家长姓名')),
                ('wechat', models.CharField(help_text='QQ/微信/电话', max_length=64, unique=True, verbose_name='联系方式')),
                ('source', models.SmallIntegerField(choices=[(1, '广告'), (2, '学员介绍'), (3, '微信好友'), (4, '其他')], default=1, verbose_name='来源')),
                ('status', models.IntegerField(choices=[(1, '已报名'), (2, '未报名')], default=2, help_text='学生是否报名', verbose_name='状态')),
                ('remark', models.TextField(max_length=248, verbose_name='学生简略信息')),
                ('date', models.DateField(auto_now_add=True, verbose_name='咨询日期')),
                ('consultant', models.ForeignKey(blank=True, limit_choices_to={'depart__title': '销售部'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to='web.UserInfo', verbose_name='课程顾问')),
                ('course', models.ManyToManyField(to='web.Course', verbose_name='咨询课程')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=500, verbose_name='跟进内容')),
                ('date', models.DateField(auto_now_add=True, verbose_name='跟进日期')),
                ('consultant', models.ForeignKey(limit_choices_to={'depart__title': '销售部'}, on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='跟踪人')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Customer', verbose_name='跟进的客户')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('userinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.UserInfo')),
                ('course', models.ManyToManyField(to='web.Course', verbose_name='科目')),
            ],
            options={
                'abstract': False,
            },
            bases=('web.userinfo',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('userinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.UserInfo')),
                ('stu_name', models.CharField(max_length=32, verbose_name='学生姓名')),
                ('sex', models.IntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('education', models.IntegerField(blank=True, choices=[(1, '小学'), (2, '初中'), (3, '高中')], null=True, verbose_name='年级')),
                ('school', models.CharField(blank=True, max_length=64, null=True, verbose_name='学校')),
                ('course', models.ManyToManyField(to='web.Course', verbose_name='课程')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Customer', verbose_name='客户信息')),
                ('teacher', models.ManyToManyField(blank=True, limit_choices_to={'depart__name': '教学部'}, null=True, to='web.Teacher', verbose_name='任课老师')),
            ],
            options={
                'abstract': False,
            },
            bases=('web.userinfo',),
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_num', models.PositiveIntegerField(verbose_name='节次')),
                ('date', models.DateField(verbose_name='上课日期')),
                ('knowledge_points', models.TextField(verbose_name='授课知识点')),
                ('execption', models.TextField(verbose_name='下节课展望或作业')),
                ('status', models.IntegerField(choices=[(1, '已审核'), (2, '未审核'), (3, '已驳回')], default=2, verbose_name='状态')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course', verbose_name='科目')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student', verbose_name='学生姓名')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Teacher', verbose_name='讲师')),
            ],
        ),
    ]
