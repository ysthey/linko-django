# Generated by Django 3.0.7 on 2020-07-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_auto_20200726_0448'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
    ]
