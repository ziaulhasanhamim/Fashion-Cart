# Generated by Django 3.1 on 2021-05-06 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_exclusiveproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exclusiveproduct',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.product'),
        ),
    ]