# Generated by Django 3.0.5 on 2020-04-04 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='manager',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
