from django.contrib import admin

from exam_prep_three.main_app.models import TennisPlayer


@admin.register(TennisPlayer)
class TennisPlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'country', 'ranking', 'is_active']
    list_filter = ['is_active']
    search_fields = ['full_name', 'country']


