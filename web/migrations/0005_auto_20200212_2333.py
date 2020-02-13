# Generated by Django 3.0.3 on 2020-02-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20200212_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='email',
        ),
        migrations.AddField(
            model_name='teacher',
            name='wechat',
            field=models.CharField(default=1, max_length=32, verbose_name='微信'),
            preserve_default=False,
        ),
    ]