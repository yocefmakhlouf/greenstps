# Generated by Django 4.0.5 on 2022-07-02 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_last_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='last_users',
            name='date',
            field=models.DateTimeField(),
        ),
    ]