#command python manage.py makemigrations main_app --name migrate_unique_brands --empty
#resut 0003_migrate_unique_brands
#logic for adding unique brands
#logic for reversing operations

from django.db import migrations


def create_unique_brands(apps, schema_editor):
    shoe = apps.get_model('main_app', 'Shoe')
    unique_brands = apps.get_model('main_app', 'UniqueBrands')

    unique_brand_names = shoe.objects.values_list('brand', flat=True).distinct()

    unique_brands.objects.bulk_create([unique_brands(brand=brand_name) for brand_name in unique_brand_names])


def reverse_unique_brands(apps, schema_editor):
    unique_brands = apps.get_model('main_app', 'UniqueBrands')
    unique_brands.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [migrations.RunPython(create_unique_brands, reverse_unique_brands)
    ]

