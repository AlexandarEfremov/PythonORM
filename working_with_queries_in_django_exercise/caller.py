import os
from typing import List
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import ArtworkGallery, Laptop, OSChoices, ChessPlayer


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
    Laptop.objects.filter(brand="Asus").update(operation_system=OSChoices.WINDOWS)
    Laptop.objects.filter(brand="Apple").update(operation_system=OSChoices.MACOS)
    Laptop.objects.filter(brand__in=("Dell", "Acer")).update(operation_system=OSChoices.LINUX)
    Laptop.objects.filter(brand="Lenovo").update(operation_system=OSChoices.CHROME_OS)


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


#3. Chess


def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(rating__range=(2399, 2300)).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filter(rating__range=(2299, 2200)).update(title='FM')


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(rating__range=(2299, 0)).update(title="regular player")
