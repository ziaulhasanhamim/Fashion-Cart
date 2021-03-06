# Generated by Django 3.1 on 2021-05-21 03:28

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('featured_in', models.CharField(choices=[('men', 'Men'), ('women', 'Women'), ('none', 'None')], default='none', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(blank=True, null=True)),
                ('date_delivered', models.DateTimeField(blank=True, null=True)),
                ('cancellion_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Not Ordered'), (1, 'Pending'), (2, 'Processing'), (3, 'Delivered'), (-1, 'Cancelled')], default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('summary', models.TextField(max_length=1000)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('thumbnail', models.ImageField(upload_to='product_thumbnails/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('for_gender', models.CharField(choices=[('men', 'Men'), ('women', 'Women'), ('both', 'Both')], default='men', max_length=10)),
                ('sold', models.IntegerField(default=0)),
                ('url', models.SlugField(blank=True, null=True, unique=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='core.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAndBilling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('payment_option', models.IntegerField(choices=[(1, 'Bkash'), (2, 'Cash On Delivery')], default=1)),
                ('bkash_number', models.CharField(blank=True, max_length=20, null=True)),
                ('shipping_charge', models.IntegerField(default=0)),
            ],
        ),
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
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(choices=[(1, '1'), (1.5, '1.5'), (2.5, '2.5'), (3, '3'), (3.5, '3.5'), (4, '4'), (4.5, '4.5'), (5, '5')])),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='core.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='core.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='core.shippingandbilling'),
        ),
        migrations.CreateModel(
            name='ExclusiveProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_till', models.DateTimeField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
    ]
