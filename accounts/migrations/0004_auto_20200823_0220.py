# Generated by Django 3.1 on 2020-08-23 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200818_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(max_length=100000, null=True),
        ),
    ]
