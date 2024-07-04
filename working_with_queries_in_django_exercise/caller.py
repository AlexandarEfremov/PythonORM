import os
from typing import List

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import ArtworkGallery, Laptop


#1. Artwork Gallery


def show_highest_rated_art():
    high_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{high_art.art_name} is the highest-rated art with a {high_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


#2. Laptop


def show_the_most_expensive_laptop():
    most_ex = Laptop.objects.order_by('-price', '-id').first()
    return f'{most_ex.brand} is the most expensive laptop available for {most_ex.price}$!'


def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems():
    all_pcs = Laptop.objects.all()
    for pc in all_pcs:
        if pc.brand == 'Asus':
            pc.operation_system = 'Windows'
        elif pc.brand == 'Apple':
            pc.operation_system = 'MacOS'
        elif pc.brand in ['Dell', 'Acer']:
            pc.operation_system = 'Linux'
        else:
            pc.operation_system = 'Chrome OS'
        pc.save()


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#
#     brand='Asus',
#
#     processor='Intel Core i5',
#
#     memory=8,
#
#     storage=256,
#
#     operation_system='MacOS',
#
#     price=899.99
# )
#
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16, storage=256,
#     operation_system='MacOS',
#     price=1399.99 )
#
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
#
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
#
# update_operation_systems()
#
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

