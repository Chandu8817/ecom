# Generated by Django 3.1.7 on 2021-04-12 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210410_0547'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': (('can_add_product', 'can add product'),)},
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order_id',
            field=models.CharField(default='1D6E64', editable=False, max_length=15, unique=True),
        ),
    ]
