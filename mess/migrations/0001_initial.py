# Generated by Django 4.2.2 on 2023-07-12 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mess',
            fields=[
                ('mess_id', models.IntegerField(primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(max_length=100)),
                ('manager_name', models.CharField(default='', max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('cost_per_day', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('rebate_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('contract_start_date', models.DateField()),
                ('contract_end_date', models.DateField()),
                ('contract_duration', models.IntegerField()),
                ('menu_image', models.ImageField(blank=True, null=True, upload_to='mess_menu')),
            ],
        ),
    ]
