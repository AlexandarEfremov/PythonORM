import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Author, Review, Article


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    name_query = Q(full_name__icontains=search_name)
    email_query = Q(email__icontains=search_email)

    if search_name and search_email:
        final_query = query
    elif search_name and search_email is None:
        final_query = name_query
    else:
        final_query = email_query

    obj = Author.objects.filter(final_query).order_by('-full_name')
    if not obj:
        return ''

    result = [f"Author: {a.full_name}, email: {a.email}, status: {'Not Banned' if a.is_banned is False else 'Banned'}"
              for a in obj]

    return "\n".join(result)


def get_top_publisher():
    obj = Author.objects.annotate(num_art=Count('article')).order_by('-num_art', 'email').first()
    if not obj or obj.num_art == 0:
        return ""

    return f"Top Author: {obj.full_name} with {obj.num_art} published articles."


def get_top_reviewer():
    obj = Author.objects.annotate(num_reviews=Count("review")).order_by("-num_reviews", "email").first()
    if not obj or obj.num_reviews == 0:
        return ""

    return f"Top Reviewer: {obj.full_name} with {obj.num_reviews} published reviews."


