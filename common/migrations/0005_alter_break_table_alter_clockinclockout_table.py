# Generated by Django 4.2.7 on 2023-11-23 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_alter_clockinclockout_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='break',
            table='break_tb',
        ),
        migrations.AlterModelTable(
            name='clockinclockout',
            table='clockinclockout_tb',
        ),
    ]