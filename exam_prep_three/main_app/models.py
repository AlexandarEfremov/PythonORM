from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(number_of_wins=Count("won_matches")).order_by('-number_of_wins', 'full_name')


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(120)
        ]
    )
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(100)
        ]
    )
    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(300)
        ]

    )
    is_active = models.BooleanField(
        default=True,
    )

    objects = TennisPlayerManager()


class Tournament(models.Model):
    class SurfaceChoices(models.TextChoices):
        NOT_SELECTED = "Not Selected", "Not Selected"
        CLAY = "Clay", "Clay"
        GRASS = "Grass", "Grass"
        HARD_COURT = "Hard Court", "Hard Court"

    name = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(150)
        ],
        unique=True
    )
    location = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(100)
        ]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    start_date = models.DateField()
    surface_type = models.CharField(
        choices=SurfaceChoices,
        max_length=12,
        validators=[
            MaxLengthValidator(12)
        ],
        default="Not Selected"
    )


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    score = models.CharField(
        max_length=100,
        validators=[
            MaxLengthValidator(100)
        ]
    )
    summary = models.TextField(
        validators=[
            MinLengthValidator(5)
        ]
    )
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(
        to="Tournament",
        on_delete=models.CASCADE,
        related_name="matches"
    )
    players = models.ManyToManyField(
        to="TennisPlayer",
        related_name="matches"
    )
    winner = models.ForeignKey(
        to="TennisPlayer",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="won_matches"
    )
