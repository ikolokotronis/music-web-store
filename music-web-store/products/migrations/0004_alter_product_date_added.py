# Generated by Django 4.0 on 2021-12-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
