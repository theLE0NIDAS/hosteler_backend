# Generated by Django 4.2.2 on 2023-07-11 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='total_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
