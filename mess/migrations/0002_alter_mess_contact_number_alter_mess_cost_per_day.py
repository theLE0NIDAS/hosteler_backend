# Generated by Django 4.2.2 on 2023-07-12 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mess',
            name='contact_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='mess',
            name='cost_per_day',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
    ]
