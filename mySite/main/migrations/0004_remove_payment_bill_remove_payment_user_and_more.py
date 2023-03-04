# Generated by Django 4.1.5 on 2023-03-04 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_bill_time_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.AddField(
            model_name='payment',
            name='address',
            field=models.CharField(default=123, max_length=100, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='cost',
            field=models.FloatField(default=132, verbose_name='Для оплаты'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='current_count',
            field=models.FloatField(default=213, verbose_name='Нынешнее значение счетчика'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='district',
            field=models.CharField(default=123, max_length=100, verbose_name='Район'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default=123, max_length=100, verbose_name='Район'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='rate_cost',
            field=models.FloatField(default=10, verbose_name='Стоимость тарифа '),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='rate_name',
            field=models.CharField(default='asd', max_length=100, verbose_name='Название тарифа'),
            preserve_default=False,
        ),
    ]
