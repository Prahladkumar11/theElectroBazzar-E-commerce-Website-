# Generated by Django 5.0.3 on 2024-03-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_customuser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='billlinggAddress',
            new_name='billingAddress',
        ),
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]