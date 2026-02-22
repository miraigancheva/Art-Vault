from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Artwork, Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'colour_hex']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Oil Painting',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of this category...',
            }),
            'colour_hex': forms.TextInput(attrs={
                'class': 'form-control form-control-color',
                'type': 'color',
            }),
        }
        labels = {
            'colour_hex': 'Badge Colour',
        }
        error_messages = {
            'name': {
                'required': 'Category name is required.',
                'unique': 'A category with this name already exists.',
            }
        }


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = [
            'title', 'artist', 'category', 'description',
            'year_created', 'medium', 'dimensions',
            'estimated_value', 'image_url', 'is_on_display',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Starry Night',
            }),
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the artwork, its significance, technique...',
            }),
            'year_created': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1889',
            }),
            'medium': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Oil on canvas',
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 73.7 × 92.1 cm',
            }),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'USD value — leave blank if unknown',
                'step': '0.01',
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/artwork.jpg',
            }),
            'is_on_display': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'image_url': 'Image URL',
            'is_on_display': 'Currently on Display',
            'year_created': 'Year Created',
            'estimated_value': 'Estimated Value (USD)',
        }
        help_texts = {
            'estimated_value': 'Leave blank if the value is unknown or not applicable.',
            'is_on_display': 'Check if this artwork is currently being displayed in the gallery.',
        }
        error_messages = {
            'title': {'required': 'The artwork must have a title.'},
            'artist': {'required': 'Please assign an artist to this artwork.'},
            'description': {'required': 'A description is required.'},
            'year_created': {
                'required': 'Year created is required.',
                'invalid': 'Please enter a valid year.',
            },
            'medium': {'required': 'Please specify the medium used.'},
        }

    def clean_year_created(self):
        year = self.cleaned_data.get('year_created')
        current_year = timezone.now().year
        if year and year > current_year:
            raise ValidationError(f'Year created cannot exceed the current year ({current_year}).')
        return year

    def clean_estimated_value(self):
        value = self.cleaned_data.get('estimated_value')
        if value is not None and value < 0:
            raise ValidationError('Estimated value cannot be negative.')
        return value


class ArtworkFilterForm(forms.Form):
    """Used on the artwork list page for filtering/sorting."""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search title or description…',
        }),
        label='Search',
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    on_display = forms.ChoiceField(
        choices=[('', 'All'), ('yes', 'On Display'), ('no', 'Not on Display')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Display Status',
    )
    sort = forms.ChoiceField(
        choices=[
            ('-year_created', 'Newest First'),
            ('year_created', 'Oldest First'),
            ('title', 'Title A–Z'),
            ('-title', 'Title Z–A'),
        ],
        required=False,
        initial='-year_created',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Sort By',
    )
