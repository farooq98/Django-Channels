# Generated by Django 3.1.1 on 2021-10-09 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20210918_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='workspace',
        ),
    ]
