# Generated by Django 5.0.4 on 2024-07-14 14:29

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_foodcriticrestaurantreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('reviewer_name', models.CharField(max_length=100)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.menu')),
            ],
            options={
                'verbose_name': 'Menu Review',
                'verbose_name_plural': 'Menu Reviews',
                'ordering': ['-rating'],
                'abstract': False,
                'indexes': [models.Index(fields=['menu'], name='main_app_menu_review_menu_id')],
                'unique_together': {('reviewer_name', 'menu')},
            },
        ),
    ]
