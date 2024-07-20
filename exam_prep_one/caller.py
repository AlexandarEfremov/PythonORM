import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg


def get_directors(search_name=None, search_nationality=None):
    result = []
    if search_name is None and search_nationality is None:
        return ''

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    query = ''

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is None and search_nationality is not None:
        query = query_nationality
    elif search_name is not None and search_nationality is None:
        query = query_name

    directors = Director.objects.filter(query).order_by('full_name')
    if not directors:
        return ''

    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, "
                      f"experience: {d.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    obj = Director.objects.annotate(most_movies=Count('movie')).order_by('-most_movies', 'full_name').first()
    if not obj:
        return ''
    return f"Top Director: {obj.full_name}, movies: {obj.most_movies}."


def get_top_actor():
    obj = (Actor.objects.annotate(most_movies_starred=Count('starred_movies'))
           .order_by('-most_movies_starred', 'full_name').first())
    if not Actor.objects.exists():
        return ''
    if not obj or obj.most_movies_starred == 0:
        return ''

    obj_avg_rating = obj.starred_movies.aggregate(avg_rating=Avg('rating'))['avg_rating']
    movie_titles = ", ".join(movie.title for movie in obj.starred_movies.all())

    return f"Top Actor: {obj.full_name}, starring in movies: {movie_titles}, movies average rating: {obj_avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(total_movies=Count('movie')).order_by('-total_movies', 'full_name')[:3]

    if not actors or not actors[0].total_movies:
        return ''

    result = [f"{act.full_name}, participated in {act.total_movies} movies"
              for act in actors]
    return "\n".join(result)


def get_top_rated_awarded_movie():
    mo = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not mo:
        return ''

    sa_name = mo.starring_actor.full_name if mo.starring_actor is not None else 'N/A'
    cast = [act.full_name for act in mo.actors.all().order_by('full_name')]
    return (f"Top rated awarded movie: {mo.title}, rating: {mo.rating}. Starring actor: {sa_name}. "
            f"Cast: {', '.join(cast)}.")
