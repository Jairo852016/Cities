# Generated by Django 3.2.9 on 2022-04-08 17:28

from enum import unique
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('citie', models.CharField(max_length=255, unique=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('country', models.CharField(max_length=255)),
                ('iso2', models.CharField(max_length=3)),
                ('admin_name', models.CharField(max_length=255)),
                ('capital', models.CharField(max_length=255)),
                ('population', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('population_proper', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]