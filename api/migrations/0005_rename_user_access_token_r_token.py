# Generated by Django 4.0.5 on 2022-06-30 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_refresh_token_access_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='access_token',
            old_name='user',
            new_name='r_token',
        ),
    ]
