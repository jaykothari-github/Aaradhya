# Generated by Django 4.2.20 on 2025-03-15 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='role',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Sir', 'Sir'), ('Student', 'Student')], default='Student', max_length=10),
        ),
    ]
