# Generated by Django 3.0.5 on 2020-04-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_address_suburb'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='suburb',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]