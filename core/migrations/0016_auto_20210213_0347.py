# Generated by Django 3.1.5 on 2021-02-13 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_product_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]