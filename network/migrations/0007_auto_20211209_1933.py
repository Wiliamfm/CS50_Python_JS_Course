# Generated by Django 3.2.6 on 2021-12-10 00:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_post_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 10, 0, 33, 23, 859145, tzinfo=utc)),
        ),
    ]
