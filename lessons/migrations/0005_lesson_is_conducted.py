# Generated by Django 5.1.6 on 2025-02-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0004_lesson_description_lesson_materials'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_conducted',
            field=models.BooleanField(blank=True, null=True, verbose_name='Conducted'),
        ),
    ]
