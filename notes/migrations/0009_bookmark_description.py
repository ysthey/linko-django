# Generated by Django 3.0.7 on 2020-07-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_contact_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]