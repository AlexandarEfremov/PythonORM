#command python manage.py makemigrations main_app --name migrate_unique_brands --empty
#resut 0003_migrate_unique_brands

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
    ]
