# Generated by Django 4.2.2 on 2023-07-10 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('complaint_id', models.IntegerField(primary_key=True, serialize=False)),
                ('category', models.CharField(choices=[('ELECTRICAL', 'Electrical'), ('PLUMBING', 'Plumbing'), ('CARPENTRY', 'Carpentry'), ('SANITATION', 'Sanitation'), ('OTHERS', 'Others')], default='OTHERS', max_length=15)),
                ('location', models.CharField(default='', max_length=50)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved')], default='PENDING', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
    ]
