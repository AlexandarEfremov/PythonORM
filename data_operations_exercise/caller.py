import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location
from main_app import apps


def create_pet(name: str, species: str):
    pet = Pet(
        name=name,
        species=species
    )

    pet.save()

    return f"{name} is a very cute {species}!"

# Create queries within functions

# Commands
# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    artifact = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    artifact.save()

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    result = ''
    all_locations = Location.objects.all().order_by('-id')

    return '\n'.join(f'{l.name} has a population of {l.population}!' for l in all_locations)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    all_capitals = Location.objects.filter(is_capital=True)
    return all_capitals


def delete_first_location():
    Location.objects.first().delete()

