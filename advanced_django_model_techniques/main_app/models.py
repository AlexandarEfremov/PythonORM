from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields import validators


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Name must be at least 2 characters long."),
            MaxLengthValidator(100, "Name cannot exceed 100 characters.")
        ])
    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2, "Location must be at least 2 characters long."),
            MaxLengthValidator(200, "Location cannot exceed 200 characters."),
        ])
    description = models.TextField(
        blank=True,
        null=True,
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, "Rating must be at least 0.00."),
            MaxValueValidator(5.00, "Rating cannot exceed 5.00.")
        ]
    )


def validate_menu_categories(value):
    categories = ["Appetizers", "Main Course", "Desserts"]
    for cat in categories:
        if cat not in value:
            raise ValidationError(
                'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')


class Menu(models.Model):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        validators=[validate_menu_categories]
    )
    restaurant = models.ForeignKey(
        to='Restaurant',
        on_delete=models.CASCADE,
    )


class RestaurantReview(models.Model):
    reviewer_name = models.CharField(
        max_length=100,
    )
    restaurant = models.ForeignKey(
        to='Restaurant',
        on_delete=models.CASCADE,
    )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5)
        ]
    )

    class Meta:
        abstract = True
        ordering = ['-rating']
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ["reviewer_name", "restaurant"]


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview.Meta):
    food_critic_cuisine_area = models.CharField(
        max_length=100,
    )

    class Meta:
        verbose_name = "Food Critic Review"
        verbose_name_plural = "Food Critic Reviews"




# Create your models here.
