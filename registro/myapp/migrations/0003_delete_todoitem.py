# Generated by Django 5.0 on 2023-09-16 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_token'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TodoItem',
        ),
    ]
