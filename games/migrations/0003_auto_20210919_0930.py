# Generated by Django 3.1.7 on 2021-09-19 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20210919_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionsoptions',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='games.questions'),
        ),
    ]
