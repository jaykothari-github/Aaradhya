# Generated by Django 4.2.20 on 2025-03-15 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_profile_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_qr',
            field=models.FileField(default='profile_qr/default.png', upload_to='profile_qr/'),
        ),
    ]
