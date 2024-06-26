from django.db import models


class Shoe(models.Model):
    brand = models.CharField(max_length=25)
    size = models.PositiveIntegerField()

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0001_initial.py


class UniqueBrands(models.Model):
    brand = models.CharField(max_length=25, unique=True)
    size = models.PositiveIntegerField()

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0002_uniquebrands.py


class EventRegistration(models.Model):
    event_name = models.CharField(max_length=60)
    participant_name = models.CharField(max_length=50)
    registration_date = models.DateField()

    def __str__(self):
        return f"{self.participant_name} - {self.event_name}"

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0004_eventregistration.py


class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    release_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50)

    def __str__(self):
        return f'Movie "{self.title}" by {self.director}'


#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0005_movie.py

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=10)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0006_student.py


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.phone}"

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0007_supplier.py


class Course(models.Model):
    title = models.CharField(max_length=90)
    lecturer = models.CharField(max_length=90)
    description = models.TextField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.lecturer}"

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0008_course.py