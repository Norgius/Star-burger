# Generated by Django 3.2.15 on 2023-01-06 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='звонок заказчику'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='доставлен'),
        ),
        migrations.AddField(
            model_name='order',
            name='registration_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='зарегистрирован'),
        ),
    ]
