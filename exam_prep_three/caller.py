import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import TennisPlayer, Match, Tournament


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

    return f"Top Tennis Player: {player.full_name} with {player.m_wins} wins."


def get_tennis_player_by_matches_count():
    if not TennisPlayer.objects.exists() or not Match.objects.exists():
        return ""

    player = TennisPlayer.objects.annotate(
        most_matches=Count("matches")
    ).order_by(
        "-most_matches",
        "ranking"
    ).first()

    if not player:
        return ""

    return f"Tennis Player: {player.full_name} with {player.most_matches} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None or not Tournament.objects.exists():
        return ""

    tournament = Tournament.objects.annotate(
        num_matches=Count("matches")
    ).filter(
        surface_type__icontains=surface
    ).order_by(
        "-start_date"
    )

    if not tournament:
        return ""

    return "\n".join(f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}" for t in tournament)
