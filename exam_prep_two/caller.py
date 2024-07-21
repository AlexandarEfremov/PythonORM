import os
from decimal import Decimal

import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order, Product


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


def get_last_sold_products():
    obj = Order.objects.order_by('-creation_date').prefetch_related('products').first()

    if not obj:
        return ''

    all_prods = ', '.join([prod.name for prod in obj.products.all().order_by('name')])
    result = f"Last sold products: {all_prods}"
    return result


def get_top_products():
    obj = Product.objects.annotate(num_sold=Count('order')).filter(num_orders__gt=0).order_by('-num_sold', 'name')[:5]

    if not obj:
        return ''

    prod_info = [f"{prod.name}, sold {prod.num_sold}" for prod in obj]
    result = "Top products:\n" + '\n'.join(prod_info)

    return result


def apply_discounts():
    obj = Order.objects.annotate(num_of_products=Count('products')).filter(num_of_products__gt=2, is_completed=False)
    discount = F('total_price') * Decimal('0.9')

    obj.update(total_price=discount)

    if obj.count() != 0:
        return f"Discount applied to {obj.count()} orders."
    f"Discount applied to {0} orders."

