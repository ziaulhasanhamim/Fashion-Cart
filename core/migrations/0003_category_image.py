# Generated by Django 3.1.5 on 2021-01-29 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210129_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null='true', upload_to='category_images/'),
            preserve_default='true',
        ),
    ]