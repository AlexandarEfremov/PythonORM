import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""
    main_query = ""

    both_query = Q(full_name__icontains=search_name) & Q(country__icontains=search_country)
    name_query = Q(full_name__icontains=search_name)
    country_query = Q(country__icontains=search_country)

    if search_name and search_country:
        main_query = both_query
    elif search_name is None and search_country:
        main_query = country_query
    elif search_country is None and search_name:
        main_query = name_query

    player = TennisPlayer.objects.filter(main_query).order_by("ranking")

    if not player:
        return ""

    return "\n".join(f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}" for p in player)


def get_top_tennis_player():
    if not TennisPlayer.objects.exists():
        return ""

    player = TennisPlayer.objects.annotate(
        m_wins=Count("won_matches")
    ).order_by(
        "-m_wins",
        "full_name"
    ).first()

    if not player:
        return ""

    return (f"Top Tennis Player: {p.full_name} with {p.m_wins} wins." for p in player)

