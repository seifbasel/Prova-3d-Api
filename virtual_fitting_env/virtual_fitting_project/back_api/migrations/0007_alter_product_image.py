# Generated by Django 5.0 on 2024-07-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_api', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(),
        ),
    ]
