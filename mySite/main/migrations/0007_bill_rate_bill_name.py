# Generated by Django 4.1.5 on 2023-03-01 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_bill_rate_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_rate',
            name='bill_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.bill_name'),
            preserve_default=False,
        ),
    ]