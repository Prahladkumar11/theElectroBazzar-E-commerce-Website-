# Generated by Django 5.0.3 on 2024-03-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_alter_order_orderid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='createdDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
