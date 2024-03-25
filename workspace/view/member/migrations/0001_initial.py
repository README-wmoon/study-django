# Generated by Django 5.0.2 on 2024-02-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_email', models.TextField()),
                ('member_password', models.TextField()),
                ('member_name', models.TextField()),
            ],
            options={
                'db_table': 'tbl_member',
            },
        ),
    ]
