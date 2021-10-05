# Generated by Django 3.2.7 on 2021-10-04 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255, unique=True)),
                ('room_capacity', models.PositiveSmallIntegerField()),
                ('projector_available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoomReservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace_booking.room')),
            ],
            options={
                'unique_together': {('room', 'date')},
            },
        ),
    ]
