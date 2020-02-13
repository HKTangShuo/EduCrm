# Generated by Django 3.0.3 on 2020-02-12 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20200212_2343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saler',
            fields=[
                ('userinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.UserInfo')),
            ],
            options={
                'abstract': False,
            },
            bases=('web.userinfo',),
        ),
        migrations.AlterField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to='web.Saler', verbose_name='课程顾问'),
        ),
    ]
