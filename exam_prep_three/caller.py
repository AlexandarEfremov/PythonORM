import os
import django
from django.db.models import Q, Count, Avg

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
    obj = Author.objects.annotate(num_reviews=Count("reviews")).order_by("-num_reviews", "email").first()
    if not obj or obj.num_reviews == 0:
        return ""

    return f"Top Reviewer: {obj.full_name} with {obj.num_reviews} published reviews."


def get_latest_article():
    article = Article.objects.annotate(
        total_reviews=Count("reviews"),
        avg_rating=Avg("reviews__rating")
    ).order_by("-published_on").first()

    if article:
        authors = ", ".join(a.full_name for a in article.authors.all().order_by("full_name"))
        avg = article.avg_rating or 0

        return f"The latest article is: {article.title}. Authors: {authors}. Reviewed: {article.total_reviews} times." \
               f" Average Rating: {avg:.2f}."

    return ""

# article = Article.objects.prefetch_related("authors", "reviews").order_by("-published_on").first()
#
#     if article:
#
#         authors = ", ".join(a.full_name for a in article.authors.all().order_by("full_name"))
#         avg_rating = article.reviews.aggregate(avg_rating=Avg("rating"))["avg_rating"] or 0
#         total_reviews = article.reviews.count()
#
#         return f"The latest article is: {article.title}. Authors: {authors}. Reviewed: {total_reviews} times." \
#                f" Average Rating: {avg_rating:.2f}."
#
#     return ""


    # latest_article = Article.objects.order_by('-published_on').first()
    #
    # if latest_article:
    #     authors_names = ', '.join(sorted([author.full_name for author in latest_article.authors.all()]))
    #
    #     num_reviews = latest_article.reviews.count()
    #     avg_rating = latest_article.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    #
    #     return (f"The latest article is: {latest_article.title}. Authors: {authors_names}. "
    #             f"Reviewed: {num_reviews} times. Average Rating: {avg_rating:.2f}.")
    #
    # return ""
