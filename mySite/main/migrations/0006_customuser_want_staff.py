# Generated by Django 4.1.5 on 2023-02-20 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_report_time_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='want_staff',
            field=models.BooleanField(default='False', verbose_name='Хочет быть админом'),
        ),
    ]