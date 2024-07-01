import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
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
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount():
    all_cars = Car.objects.all()
    for car in all_cars:
        percentage = sum(int(digit) for digit in str(car.year)) / 100
        discount = float(car.price) * percentage
        car.price_with_discount = float(car.price) - discount
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car():
    Car.objects.last().delete()


########################################

def show_unfinished_tasks():
    unfinished_tasks = Task.objects.all().filter(is_finished=False)
    return '\n'.join(f"Task - {task.title} needs to be done until {task.due_date}!" for task in unfinished_tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()
    for task in tasks:
        if task.id % 2 != 0:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    decoded_text = ''.join(chr(ord(symbol) - 3) for symbol in text)
    Task.objects.filter(title=task_title).update(description=decoded_text)


#################################


def get_deluxe_rooms():
    all_rooms = HotelRoom.objects.all()
    result = []
    for room in all_rooms:
        if room.id % 2 == 0 and room.room_type == 'Deluxe':
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")
    return '\n'.join(result)


def increase_room_capacity():
    all_reserved_rooms = HotelRoom.objects.all().order_by('id')

    previous_room_capacity = None

    for room in all_reserved_rooms:
        if not room.is_reserved:
            continue

        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id
        previous_room_capacity = room.capacity

        room.save()


def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()


def delete_last_room():
    last_room = HotelRoom.objects.last()
    if not last_room.is_reserved:
        HotelRoom.objects.last().delete()


#########################


def update_characters():
    all_chars = Character.objects.all()
    updated_chars = []

    for person in all_chars:
        if person.class_name == "Mage":
            person.level += 3
            person.intelligence -= 7
        elif person.class_name == "Warrior":
            person.hit_points /= 2
            person.dexterity += 4
        elif person.class_name == "Scout" or person.class_name == "Assassin":
            person.inventory = "The inventory is empty"
        updated_chars.append(person)

    if updated_chars:
        fields_to_update = ['level', 'intelligence', 'hit_points', 'dexterity', 'inventory']
        Character.objects.bulk_update(updated_chars, fields_to_update)


def fuse_characters(first_character: Character, second_character: Character):
    new_character = Character(
        name=f'{first_character.name} {second_character.name}',
        class_name="Fusion",
        level=int((first_character.level + second_character.level) // 2),
        strength=int((first_character.strength + second_character.strength) * 1.2),
        dexterity=int((first_character.dexterity + second_character.dexterity) * 1.4),
        intelligence=int((first_character.intelligence + second_character.intelligence) * 1.5),
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=("Bow of the Elven Lords, Amulet of Eternal Wisdom" if first_character.class_name in ["Mage", "Scout"]
                   else "Dragon Scale Armor, Excalibur")
    )
    new_character.save()
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.all().filter(inventory="The inventory is empty").delete()


