# Generated by Django 4.1.5 on 2023-02-23 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0023_alter_brand_image_name_alter_product_image_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='warehouseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_type_title', models.CharField(max_length=50, verbose_name='warehouse type')),
            ],
            options={
                'verbose_name': 'warehouse type',
                'verbose_name_plural': 'warehouses type',
            },
        ),
        migrations.CreateModel(
            name='warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_warehouses', to='products.product')),
                ('user_registered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_warehouses', to=settings.AUTH_USER_MODEL)),
                ('warehouse_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='warehouses.warehousetype')),
            ],
            options={
                'verbose_name': 'warehouse',
                'verbose_name_plural': 'warehouses',
            },
        ),
    ]