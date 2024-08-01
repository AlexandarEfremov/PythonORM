from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models


class DateTime(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )
    email = models.EmailField(
        unique=True
    )
    is_banned = models.BooleanField(
        default=False
    )
    birth_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2005)
        ]
    )
    website = models.URLField(
        blank=True,
        null=True,
    )


class Article(DateTime):
    class ArticleCategories(models.TextChoices):
        TECHNOLOGY = "Technology", "Technology"
        SCIENCE = "Science", "Science"
        EDUCATION = "Education", "Education"

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(5)
        ]
    )
    content = models.TextField(
        validators=[
            MinLengthValidator(10)
        ]
    )
    category = models.CharField(
        choices=ArticleCategories,
        max_length=10,
        default="Technology",
    )
    authors = models.ManyToManyField(
        to='Author',
        related_name='articles'
    )


class Review(DateTime):
    content = models.TextField(
        validators=[
            MinLengthValidator(10)
        ]
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )
    author = models.ForeignKey(
        to="Author",
        related_name="reviews",
        on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        to="Article",
        related_name="reviews",
        on_delete=models.CASCADE
    )

































