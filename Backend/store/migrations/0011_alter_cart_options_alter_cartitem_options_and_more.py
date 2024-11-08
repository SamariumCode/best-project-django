# Generated by Django 5.1.2 on 2024-10-25 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_cart_alter_comment_product_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'سبد خرید', 'verbose_name_plural': 'سبدهای خرید'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'آیتم سبد خرید', 'verbose_name_plural': 'آیتم\u200cهای سبد خرید'},
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.cart', verbose_name='سبد خرید'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='نام مستعار'),
        ),
    ]
