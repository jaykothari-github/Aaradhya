# Generated by Django 4.2.20 on 2025-03-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_aadhar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_image',
            field=models.FileField(default='default/profile.jpg', upload_to='profile/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_qr',
            field=models.FileField(default='default/qr.png', upload_to='profile_qr/'),
        ),
    ]
