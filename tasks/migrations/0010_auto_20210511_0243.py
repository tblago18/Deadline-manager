# Generated by Django 3.0 on 2021-05-11 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20210511_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='notes',
            field=models.CharField(default='', max_length=500),
        ),
    ]
