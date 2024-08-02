import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count
from main_app.models import Author, Article


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    main_query = None

    both_queries = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    name_query = Q(full_name__icontains=search_name)
    email_query = Q(email__icontains=search_email)

    if search_name and search_email:
        main_query = both_queries
    elif search_name and search_email is None:
        main_query = name_query
    elif search_name is None and search_email:
        main_query = email_query

    author = Author.objects.filter(main_query).order_by(
        "-full_name"
    )

    if not author:
        return ""

    return "\n".join(f"Author: {a.full_name}, "
                     f"email: {a.email}, "
                     f"status: {'Banned' if a.is_banned else 'Not Banned'}" for a in author)


def get_top_publisher():
    if not Article.objects.exists():
        return ""

    author = Author.objects.annotate(most_art=Count("articles")).order_by(
        "-most_art",
        "email"
    ).first()

    if not author:
        return ""

    return f"Top Author: {author.full_name} with {author.most_art} published articles."


