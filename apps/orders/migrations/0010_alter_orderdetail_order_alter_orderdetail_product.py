# Generated by Django 4.1.5 on 2024-01-01 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_alter_brand_image_name_alter_product_image_name_and_more'),
        ('orders', '0009_alter_orderdetail_order_alter_orderdetail_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_Details', to='orders.order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_details', to='products.product', verbose_name='Product'),
        ),
    ]
