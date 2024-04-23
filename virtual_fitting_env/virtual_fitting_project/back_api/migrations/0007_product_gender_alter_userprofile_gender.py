# Generated by Django 5.0 on 2024-04-14 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_api', '0006_remove_cartitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'both')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'both')], default='B', max_length=1),
        ),
    ]