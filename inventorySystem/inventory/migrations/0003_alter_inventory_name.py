# Generated by Django 4.2.18 on 2025-01-29 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_inventory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
