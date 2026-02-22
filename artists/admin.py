from django.contrib import admin
from .models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_year', 'death_year', 'get_artwork_count')
    list_filter = ('nationality',)
    search_fields = ('name', 'biography')
    readonly_fields = ('created_at', 'updated_at')

    def get_artwork_count(self, obj):
        return obj.get_artwork_count()
    get_artwork_count.short_description = 'Artworks'
