# Generated by Django 3.0.7 on 2020-07-26 04:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_auto_20200726_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='note',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
    ]
