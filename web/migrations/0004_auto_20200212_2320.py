# Generated by Django 3.0.3 on 2020-02-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200212_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ManyToManyField(to='web.Teacher', verbose_name='任课老师'),
        ),
    ]
