# Generated by Django 3.1.5 on 2021-02-05 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210203_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_tagline', models.CharField(max_length=200)),
                ('secondary_tagline', models.CharField(blank=True, max_length=100, null=True)),
                ('important_text', models.CharField(blank=True, max_length=300, null=True)),
                ('starting_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('link', models.CharField(blank=True, max_length=500, null=True)),
                ('link_text', models.CharField(blank=True, max_length=30, null=True)),
                ('image', models.ImageField(upload_to='sliders/')),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
    ]
