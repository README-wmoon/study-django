# Generated by Django 5.0.2 on 2024-02-20 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_member_created_date_member_updated_date'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='member.member'),
            preserve_default=False,
        ),
    ]
