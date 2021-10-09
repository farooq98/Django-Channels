# Generated by Django 3.1.1 on 2021-10-09 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_remove_post_workspace'),
        ('user_registration', '0015_auto_20210919_0642'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workspacemodel',
            name='user',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='designation',
            new_name='user_type',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='is_workspace_admin',
        ),
        migrations.DeleteModel(
            name='UserWorkSpaceRelationTable',
        ),
        migrations.DeleteModel(
            name='WorkSpaceModel',
        ),
    ]