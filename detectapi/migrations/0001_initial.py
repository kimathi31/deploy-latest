# Generated by Django 4.0.5 on 2022-06-08 10:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='crop_diseases',
            fields=[
                ('nameid', models.IntegerField(primary_key=True, serialize=False)),
                ('disease', models.CharField(max_length=255)),
                ('symptoms', models.CharField(max_length=255)),
                ('measures', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='detection',
            fields=[
                ('Analysis_REF_No', models.AutoField(primary_key=True, serialize=False)),
                ('Crop', models.CharField(max_length=255)),
                ('Disease', models.CharField(max_length=255)),
                ('Date_Created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
