import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count
from main_app.models import Author, Review


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


# def get_top_publisher():
#     top_author = Author.objects.annotate(count_articles=Count("articles")).order_by("-count_articles", "email").first()
#
#     if not top_author or top_author.count_articles <= 0:
#         return ""
#
#     return f"Top Author: {top_author.full_name} with {top_author.count_articles} published articles."
#

def get_top_publisher():
    obj = Author.objects.annotate(num_art=Count('article')).order_by('-num_art', 'email').first()
    if not obj or obj.num_art == 0:
        return ""

    return f"Top Author: {obj.full_name} with {obj.num_art} published articles."


def get_top_reviewer():
    if not Review.objects.exists():
        return ""

    author = Author.objects.annotate(most_reviews=Count("reviews")).order_by(
        "-most_reviews",
        "email"
    ).first()

    if author:
        return f"Top Reviewer: {author.full_name} with {author.most_reviews} published reviews."

    return ""

