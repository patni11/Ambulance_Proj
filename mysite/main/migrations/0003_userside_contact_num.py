# Generated by Django 3.2 on 2021-05-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userside'),
    ]

    operations = [
        migrations.AddField(
            model_name='userside',
            name='contact_num',
            field=models.DecimalField(decimal_places=0, default=23, max_digits=10),
            preserve_default=False,
        ),
    ]
