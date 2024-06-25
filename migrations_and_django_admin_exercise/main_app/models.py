from django.db import models


class Shoe(models.Model):
    brand = models.CharField(max_length=25)
    size = models.PositiveIntegerField()

#Commands executed:
#python manage.py makemigrations
#python manage.py migrate

#result 0001_initial.py 0002_migrate_unique_brands