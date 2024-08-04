from django.core.validators import MinLengthValidator, DecimalValidator, RegexValidator, MinValueValidator
from django.db import models
from django.db.models import Count


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return self.annotate(total_missions=Count("missions")).order_by("-total_missions", "phone_number")


class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[
            RegexValidator(regex=r'^\d+$')
        ]
    )
    is_active = models.BooleanField(
        default=True
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True
    )
    spacewalks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    manufacturer = models.CharField(
        max_length=100
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )
    launch_date = models.DateField()
    updated_at = models.DateTimeField(
        auto_now=True
    )


class Mission(models.Model):
    class StatusChoices(models.TextChoices):
        PLANNED = "Planned", "Planned"
        ONGOING = "Ongoing", "Ongoing"
        COMPLETED = "Completed", "Completed"

    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    status = models.CharField(
        choices=StatusChoices,
        max_length=9,
        default="Planned"
    )
    launch_date = models.DateField()
    updated_at = models.DateTimeField(
        auto_now=True
    )
    spacecraft = models.ForeignKey(
        to="Spacecraft",
        related_name="missions",
        on_delete=models.CASCADE
    )
    astronauts = models.ManyToManyField(
        to="Astronaut",
        related_name="missions"
    )
    commander = models.ForeignKey(
        to="Astronaut",
        related_name="mission_commander",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

