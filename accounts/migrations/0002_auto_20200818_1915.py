# Generated by Django 3.1 on 2020-08-18 19:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Order Delivered', 'Order Delivered'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Indoor/Outdoor', 'Indoor/Outdoor')], max_length=200, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(max_length=1000, null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
