# Generated by Django 4.2.7 on 2023-11-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClockInClockOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('clock_type', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
