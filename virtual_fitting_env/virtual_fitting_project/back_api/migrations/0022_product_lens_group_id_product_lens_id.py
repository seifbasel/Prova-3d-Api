# Generated by Django 5.0 on 2024-06-15 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_api', '0021_remove_product_lens_group_id_remove_product_lens_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lens_group_id',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='lens_id',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
    ]
