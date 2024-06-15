# Generated by Django 5.0 on 2024-06-15 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_api', '0019_comment_sentiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lens_group_id',
            field=models.CharField(default=12, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='lens_id',
            field=models.CharField(default=12, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('S', 'small'), ('M', 'medium'), ('L', 'large'), ('XL', 'x large'), ('XXL', 'xx large')], max_length=10),
        ),
    ]
