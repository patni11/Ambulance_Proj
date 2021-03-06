# Generated by Django 3.2 on 2021-05-04 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ambulance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ambulance_state', models.BooleanField()),
                ('ambulance_lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('ambulance_long', models.DecimalField(decimal_places=6, max_digits=10)),
                ('ambulance_free_est_time', models.DateTimeField(verbose_name='Estimated Time for Next Patient')),
                ('ambulance_pickup_time', models.DateTimeField(verbose_name='Pickup Time')),
            ],
        ),
    ]
