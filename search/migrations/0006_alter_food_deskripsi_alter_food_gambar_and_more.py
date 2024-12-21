# Generated by Django 5.1.4 on 2024-12-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_delete_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='gambar',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='harga',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='food',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='food',
            name='restoran',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]