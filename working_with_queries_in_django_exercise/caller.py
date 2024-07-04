import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import ArtworkGallery


#1. Artwork Gallery


def show_highest_rated_art():
    high_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{high_art.art_name} is the highest-rated art with a {high_art.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery):
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


#2. Laptop



