# Generated by Django 4.2.20 on 2025-07-12 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_event_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image_alt_text',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
