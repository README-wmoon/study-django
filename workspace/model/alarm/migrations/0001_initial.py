# Generated by Django 5.0.2 on 2024-02-26 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0003_member_status'),
        ('post', '0002_post_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.post')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to='member.member')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to='member.member')),
            ],
            options={
                'db_table': 'tbl_alarm',
                'ordering': ['-id'],
            },
        ),
    ]
