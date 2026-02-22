from django import forms
from django.core.exceptions import ValidationError
from .models import Exhibition
from artworks.models import Artwork


class ExhibitionForm(forms.ModelForm):
    artworks = forms.ModelMultipleChoiceField(
        queryset=Artwork.objects.select_related('artist').order_by('title'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Featured Artworks',
        help_text='Select one or more artworks to include in this exhibition.',
    )

    class Meta:
        model = Exhibition
        fields = [
            'title', 'tagline', 'description', 'location',
            'start_date', 'end_date', 'artworks',
            'cover_image_url', 'admission_price', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Impressionism Reimagined',
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'A punchy one-liner for the exhibition…',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the theme, curatorial vision, and highlights…',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. East Wing, Gallery 4',
            }),
            'start_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d',
            ),
            'cover_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/banner.jpg',
            }),
            'admission_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'cover_image_url': 'Cover Image URL',
            'is_active': 'Publicly Visible',
            'admission_price': 'Admission Price (USD)',
        }
        help_texts = {
            'tagline': 'Optional — used as the subtitle on exhibition cards.',
            'is_active': 'Uncheck to hide from the public gallery listing.',
        }
        error_messages = {
            'title': {'required': 'Exhibition title is required.'},
            'description': {'required': 'A description is required.'},
            'location': {'required': 'Please specify the exhibition location.'},
            'start_date': {'required': 'Start date is required.'},
            'end_date': {'required': 'End date is required.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['created_at_display'] = forms.CharField(
                required=False,
                disabled=True,
                label='Created On',
                initial=self.instance.created_at.strftime('%d %B %Y'),
                widget=forms.TextInput(attrs={'class': 'form-control'}),
            )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'The closing date must be on or after the opening date.')
        admission = cleaned_data.get('admission_price')
        if admission is not None and admission < 0:
            self.add_error('admission_price', 'Admission price cannot be negative.')
        return cleaned_data
