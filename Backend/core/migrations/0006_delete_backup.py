# Generated by Django 5.1.2 on 2024-10-12 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_backup'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Backup',
        ),
    ]