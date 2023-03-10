# Generated by Django 4.1.6 on 2023-02-27 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedications', '0002_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='usertask',
            name='unique_user_task',
        ),
        migrations.RenameField(
            model_name='occupation',
            old_name='task',
            new_name='tasks',
        ),
        migrations.RenameField(
            model_name='occupation',
            old_name='user',
            new_name='users',
        ),
        migrations.RenameField(
            model_name='usertask',
            old_name='task',
            new_name='tasks',
        ),
        migrations.RenameField(
            model_name='usertask',
            old_name='user',
            new_name='users',
        ),
        migrations.AddConstraint(
            model_name='usertask',
            constraint=models.UniqueConstraint(fields=('users', 'tasks'), name='unique_users_tasks'),
        ),
    ]
