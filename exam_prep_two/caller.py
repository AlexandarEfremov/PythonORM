import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile


def get_profiles(search_string=None):
    if search_string is None:
        return ""

    query = (Q(full_name__icontains=search_string) | Q(email__icontains=search_string) |
             Q(phone_number__icontains=search_string))

    obj = Profile.objects.filter(query).annotate(total_orders=Count('order')).order_by('full_name')

    if not obj:
        return ""

    result = [(f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: "
               f"{p.total_orders}") for p in obj]

    return "\n".join(result)


def get_loyal_profiles():
    obj = Profile.objects.annotate(total_orders=Count('order')).filter(total_orders__gt=2).order_by('-total_orders')
    result = [f"Profile: {p.full_name}, orders: {p.total_orders}" for p in obj]

    return "\n".join(result)

