# Generated by Django 5.0.4 on 2024-07-14 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_foodcriticrestaurantreview_regularrestaurantreview_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FoodCriticRestaurantReview',
        ),
    ]
