# Generated by Django 5.1.2 on 2024-10-21 19:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_foodentry_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodentry',
            name='description',
            field=models.TextField(default='No description yet.'),
        ),
        migrations.AddField(
            model_name='foodentry',
            name='food',
            field=models.CharField(default='No food name yet.', max_length=255),
        ),
        migrations.AddField(
            model_name='foodentry',
            name='price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='foodentry',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]