import os
import django
from django.db.models import Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director


def get_directors(search_name=None, search_nationality=None):
    result = []

    if search_name is not None and search_nationality is not None:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)
        obj = Director.objects.filter(query).order_by('full_name')
    elif search_name is None and search_nationality is not None:
        query = Q(nationality__icontains=search_nationality)
        obj = Director.objects.filter(query).order_by('full_name')
    elif search_name is not None and search_nationality is None:
        query = Q(full_name__icontains=search_name)
        obj = Director.objects.filter(query).order_by('full_name')
    else:
        return ''

    for res in obj:
        result.append(f"Director: {res.full_name}, nationality: {res.nationality}, experience: {res.years_of_experience}")

    return "\n".join(result)

