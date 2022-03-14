# Generated by Django 3.2 on 2021-05-06 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210506_1547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='distance',
        ),
        migrations.AddField(
            model_name='patient',
            name='next_patient_to_pick_up',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_picked_up',
            field=models.BooleanField(default=False),
        ),
    ]
