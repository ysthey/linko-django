# Generated by Django 3.0.7 on 2020-07-26 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_map_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('created_date', models.DateField(auto_now_add=True)),
                ('category', models.CharField(default='tax-returns', max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='category',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.URLField(max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='Email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='Name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='Note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='map',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
