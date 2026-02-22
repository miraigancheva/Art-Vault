from django.contrib import admin
from .models import Artwork, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'colour_hex')
    search_fields = ('name',)


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'year_created', 'is_on_display')
    list_filter = ('category', 'is_on_display')
    search_fields = ('title', 'artist__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('artist',)
