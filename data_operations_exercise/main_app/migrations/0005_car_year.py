# Generated by Django 5.0.4 on 2024-07-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='year',
            field=models.PositiveIntegerField(default=300),
            preserve_default=False,
        ),
    ]
