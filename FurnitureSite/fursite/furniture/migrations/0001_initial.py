# Generated by Django 4.1.6 on 2023-07-17 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Url')),
                ('housing_material', models.CharField(max_length=255, verbose_name='Материал корпуса')),
                ('facade_material', models.CharField(max_length=255, verbose_name='Материал фасада')),
                ('housing_color', models.CharField(max_length=255, verbose_name='Цвет корпуса')),
                ('facade_color', models.CharField(max_length=255, verbose_name='Цвет фасада')),
                ('fittings', models.CharField(max_length=255, verbose_name='Фурнитура')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('views', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='furniture.category')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
