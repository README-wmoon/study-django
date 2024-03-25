# Generated by Django 5.0.2 on 2024-02-23 09:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('product_name', models.TextField()),
                ('product_price', models.BigIntegerField()),
                ('product_discount', models.FloatField(default=0)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tbl_product',
            },
        ),
    ]
