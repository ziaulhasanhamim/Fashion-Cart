# Generated by Django 3.1.5 on 2021-02-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210201_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='featured_in',
            field=models.CharField(choices=[('men', 'Men'), ('women', 'Women'), ('none', 'None')], default='none', max_length=10),
        ),
    ]