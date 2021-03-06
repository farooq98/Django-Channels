# Generated by Django 3.1.7 on 2021-09-19 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_auto_20210919_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestions',
            name='correct_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correct_answer', to='games.questionsoptions'),
        ),
        migrations.AlterField(
            model_name='userquestions',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_queestions', to='games.questions'),
        ),
        migrations.AlterUniqueTogether(
            name='userquestions',
            unique_together={('question', 'correct_answer', 'user')},
        ),
    ]
