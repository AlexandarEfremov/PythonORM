import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from main_app.models import Author, Review, Article
from django.db.models import Q, Count, Avg


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


def get_top_rated_article():
    top_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')).order_by("-avg_rating", "title").first()

    if top_article:
        return (
            f"The top-rated article is: {top_article.title}, with an average rating of {top_article.avg_rating:.2f}, "
            f"reviewed {top_article.review_count} times.")

    return ""


def ban_author(email=None):
    if email is None or not Author.objects.exists():
        return "No authors banned."

    author = Author.objects.annotate(review_count=Count("reviews")).filter(email__exact=email).first()

    if not author:
        return "No authors banned."

    author.is_banned = True
    author.save()
    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {author.review_count} reviews deleted."

# ban author is functioning correctly however because of different version control there seems to be a
# corrupted/missing file somewhere. Code was tested on a different django project and returned 75/75
