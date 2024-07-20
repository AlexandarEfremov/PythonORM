from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count


class DirectorManager(models.Manager):

    def get_directors_by_movies_count(self):
        return (self.annotate(total_movies=Count('movie'))
                .order_by('-total_movies', 'full_name'))


class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120)
        ]
    )
    birth_date = models.DateField(
        default='1900-01-01'
    )
    nationality = models.CharField(
        default='Unknown',
        max_length=50,
        validators=[
            MaxLengthValidator(50),
        ]
    )
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = DirectorManager()


class GenreChoices(models.TextChoices):
    ACTION = 'Action', 'Action'
    COMEDY = 'Comedy', 'Comedy'
    DRAMA = 'Drama', 'Drama'
    OTHER = 'Other', 'Other'


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120)
        ]
    )
    birth_date = models.DateField(
        default='1900-01-01'
    )
    nationality = models.CharField(
        default='Unknown',
        max_length=50,
        validators=[
            MaxLengthValidator(50)
        ]
    )
    is_awarded = models.BooleanField(
        default=False
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )


class Movie(models.Model):

    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(150)
        ]
    )
    release_date = models.DateField()
    storyline = models.TextField(
        blank=True,
        null=True,
    )
    genre = models.CharField(
        choices=GenreChoices,
        default='Other',
        max_length=6,
        validators=[
            MaxLengthValidator(6)
        ]
    )
    rating = models.DecimalField(
        decimal_places=1,
        default=0.0,
        max_digits=3,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0)
        ]
    )
    is_classic = models.BooleanField(
        default=False
    )
    is_awarded = models.BooleanField(
        default=False
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )
    director = models.ForeignKey(
        to='Director',
        on_delete=models.CASCADE,
    )
    starring_actor = models.ForeignKey(
        to='Actor',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='starred_movies'
    )
    actors = models.ManyToManyField(
        to='Actor'
    )

# Create your models here.
