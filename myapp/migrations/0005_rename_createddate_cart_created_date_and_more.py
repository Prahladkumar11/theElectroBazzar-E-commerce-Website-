# Generated by Django 4.2.6 on 2024-03-07 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_product_is_new'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='createdDate',
            new_name='created_date',
        ),
        migrations.AlterField(
            model_name='cart_item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]