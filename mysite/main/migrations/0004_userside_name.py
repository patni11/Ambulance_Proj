# Generated by Django 3.2 on 2021-05-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_userside_contact_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='userside',
            name='name',
            field=models.CharField(default='your name', max_length=200, verbose_name='Your Name'),
            preserve_default=False,
        ),
    ]
