# Generated by Django 4.0 on 2021-12-08 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_category_subcategory_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory_id',
        ),
    ]
