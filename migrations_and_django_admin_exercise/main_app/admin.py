from .models import EventRegistration, Movie
from django.contrib import admin


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    pass
    list_display = ('event_name', 'participant_name', 'registration_date')
    search_fields = ('event_name', 'participant_name')
    list_filter = ('event_name', 'registration_date')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'genre')
    list_filter = ('release_year', 'genre')
    search_fields = ('title', 'director')
