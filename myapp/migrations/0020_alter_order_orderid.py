# Generated by Django 5.0.3 on 2024-03-12 19:09

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_alter_order_orderid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderId',
            field=models.CharField(default=myapp.models.Order.generate_unique_order_id, editable=False, max_length=5, unique=True),
        ),
    ]