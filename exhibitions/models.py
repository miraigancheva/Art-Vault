from django.db import models
from django.core.validators import MinLengthValidator
from artworks.models import Artwork


class Exhibition(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3)],
        help_text='Exhibition title (3–255 characters).',
    )
    tagline = models.CharField(
        max_length=300,
        blank=True,
        help_text='A short promotional tagline.',
    )
    description = models.TextField(
        validators=[MinLengthValidator(20)],
        help_text='Full description of the exhibition (min 20 characters).',
    )
    location = models.CharField(
        max_length=200,
        help_text='Gallery room or external venue.',
    )
    start_date = models.DateField(help_text='Opening date of the exhibition.')
    end_date = models.DateField(help_text='Closing date of the exhibition.')
    artworks = models.ManyToManyField(
        Artwork,
        related_name='exhibitions',
        blank=True,
        help_text='Select the artworks featured in this exhibition.',
    )
    cover_image_url = models.URLField(
        blank=True,
        help_text='Optional URL to a banner/cover image.',
    )
    admission_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00,
        help_text='Admission price in USD. Enter 0 for free events.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to hide this exhibition from the public listing.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Exhibition'
        verbose_name_plural = 'Exhibitions'

    def __str__(self):
        return self.title

    def is_ongoing(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def get_duration_days(self):
        delta = self.end_date - self.start_date
        return delta.days

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date must be on or after the start date.'})
