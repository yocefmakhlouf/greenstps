# Generated by Django 4.0.6 on 2022-07-12 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_last_users_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
