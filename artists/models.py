from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.utils import timezone


class Artist(models.Model):

    class Nationality(models.TextChoices):
        AMERICAN = 'American', 'American'
        BRITISH = 'British', 'British'
        FRENCH = 'French', 'French'
        GERMAN = 'German', 'German'
        ITALIAN = 'Italian', 'Italian'
        SPANISH = 'Spanish', 'Spanish'
        DUTCH = 'Dutch', 'Dutch'
        JAPANESE = 'Japanese', 'Japanese'
        CHINESE = 'Chinese', 'Chinese'
        RUSSIAN = 'Russian', 'Russian'
        OTHER = 'Other', 'Other'

    name = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(2)],
        help_text='Full name of the artist (2–200 characters).',
    )
    nationality = models.CharField(
        max_length=50,
        choices=Nationality.choices,
        default=Nationality.OTHER,
    )
    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year)],
        help_text='Four-digit birth year.',
    )
    death_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year)],
        help_text='Leave blank if the artist is still alive.',
    )
    biography = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text='A short biography (minimum 20 characters).',
    )
    profile_image_url = models.URLField(
        blank=True,
        help_text='Optional URL to the artist\'s profile image.',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __str__(self):
        return self.name

    def get_lifespan(self):
        """Return a readable lifespan string."""
        if self.death_year:
            return f'{self.birth_year}–{self.death_year}'
        return f'b. {self.birth_year}'

    def get_artwork_count(self):
        return self.artworks.count()

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.death_year and self.death_year < self.birth_year:
            raise ValidationError({'death_year': 'Death year cannot be before birth year.'})
