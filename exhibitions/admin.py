from django.contrib import admin
from .models import Exhibition


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'location')
    filter_horizontal = ('artworks',)
    readonly_fields = ('created_at',)
