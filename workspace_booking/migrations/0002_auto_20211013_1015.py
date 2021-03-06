# Generated by Django 3.2.7 on 2021-10-13 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace_booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='building_floor',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='room',
            name='size',
            field=models.CharField(max_length=70, null=True),
        ),
    ]
