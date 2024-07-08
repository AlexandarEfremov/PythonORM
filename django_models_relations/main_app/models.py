from django.db import models


class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100,
    )
    last_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return f'The lecturer for {Subject.name} is {self.first_name} {self.last_name}.'


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
    )
    code = models.CharField(
        max_length=10,
        unique=True,
    )
    lecturer = models.ForeignKey(
        to='Lecturer',
        on_delete=models.SET_NULL,
        null=True
    )


# Create your models here.
