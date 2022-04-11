# Generated by Django 3.2.9 on 2022-04-09 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0003_update_search_vector'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitiesSearchWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
