# Generated by Django 4.2.7 on 2023-11-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_clockinclockout_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp_start', models.DateTimeField()),
                ('timestamp_end', models.DateTimeField()),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'Break',
            },
        ),
    ]