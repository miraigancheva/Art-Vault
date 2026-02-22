from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from artists.models import Artist


class Category(models.Model):
    """Artistic medium/style category (e.g. Oil Painting, Sculpture)."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    colour_hex = models.CharField(
        max_length=7,
        default='#6c757d',
        help_text='Hex colour used for UI badges (e.g. #ff5733).',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Artwork(models.Model):
    """A single artwork belonging to one artist and one category."""

    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(2)],
        help_text='Title of the artwork (2–255 characters).',
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.PROTECT,
        related_name='artworks',
        help_text='The artist who created this piece.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artworks',
    )
    description = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text='A short description of the artwork (min 10 characters).',
    )
    year_created = models.PositiveIntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(timezone.now().year)],
        help_text='Year the artwork was created.',
    )
    medium = models.CharField(
        max_length=150,
        help_text='Materials used (e.g. Oil on canvas, Bronze, Watercolour).',
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        help_text='Optional dimensions (e.g. 73 × 92 cm).',
    )
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text='Estimated market value in USD.',
    )
    image_url = models.URLField(
        blank=True,
        help_text='Optional URL to an image of the artwork.',
    )
    is_on_display = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year_created', 'title']
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'

    def __str__(self):
        return f'{self.title} ({self.year_created})'

    def get_value_display(self):
        if self.estimated_value is None:
            return 'Not appraised'
        return f'${self.estimated_value:,.2f}'

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.year_created and self.year_created > timezone.now().year:
            raise ValidationError({'year_created': 'Year created cannot be in the future.'})
