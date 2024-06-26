from .models import EventRegistration
from django.contrib import admin


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    pass
    list_display = ('event_name', 'participant_name', 'registration_date')
    search_fields = ('event_name', 'participant_name')
    list_filter = ('event_name', 'registration_date')
    # fieldsets = (
    #     ('General Information', {
    #         'fields': ('name', 'description', 'price', 'barcode')
    #     }),
    #     ('Categorization', {
    #         'fields': ('category', 'supplier')
    #     }),
    # )
    # date_hierarchy = 'created_on'

