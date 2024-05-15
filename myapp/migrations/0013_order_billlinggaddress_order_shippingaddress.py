# Generated by Django 5.0.3 on 2024-03-10 05:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_order_createddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billlinggAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.billingaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='shippingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.shippingaddress'),
        ),
    ]