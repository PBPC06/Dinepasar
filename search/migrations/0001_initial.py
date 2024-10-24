# Generated by Django 5.1.2 on 2024-10-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_makanan', models.CharField(max_length=255)),
                ('restoran', models.CharField(max_length=255)),
                ('kategori', models.CharField(max_length=100)),
                ('gambar', models.TextField()),
                ('deskripsi', models.TextField()),
                ('harga', models.PositiveIntegerField()),
                ('rating', models.FloatField()),
            ],
        ),
    ]