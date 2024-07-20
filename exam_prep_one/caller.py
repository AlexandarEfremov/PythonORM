import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor
from django.db.models import Q, Count, Avg


def get_directors(search_name=None, search_nationality=None):
    result = []
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is None and search_nationality is not None:
        query = query_nationality
    elif search_name is not None and search_nationality is None:
        query = query_name
    else:
        return ''

    directors = Director.objects.filter(query).order_by('full_name')
    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, "
                      f"experience: {d.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    if Director.objects.all() is None:
        return ''
    obj = Director.objects.annotate(most_movies=Count('movie')).order_by('full_name').first()
    return f"Top Director: {obj.full_name}, movies: {obj.most_movies}."


def get_top_actor():
    if Actor.objects.all() is None:
        return ''
    if Actor.objects.annotate(most_movies_starred=Count('starred_movies')) is None:
        return ''

    obj = Actor.objects.annotate(most_movies_starred=Count('starred_movies')).order_by('full_name').first()
    obj_avg_rating = obj.starred_movies.annotate(avg_rating=Avg('rating'))
    return (f"Top Actor: {obj.full_name}, starring in movies: {", ".join(m.starred_movies.title for m in obj)}, "
            f"movies average rating: {obj_avg_rating:.1f}")


