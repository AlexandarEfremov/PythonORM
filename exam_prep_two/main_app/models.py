from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models


class Profile(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(100),
        ]
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
        validators=[
            MaxLengthValidator(15),
        ]
    )
    address = models.TextField()
    is_active = models.BooleanField(
        default=True,
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
    )


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100),
        ]
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0.01)
        ]
    )
    in_stock = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
        ]
    )
    is_available = models.BooleanField(
        default=True,
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
    )


class Order(models.Model):
    profile = models.ForeignKey(
        to='Profile',
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(
        to='Product',
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0.01)
        ]
    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    is_completed = models.BooleanField(
        default=False,
    )



