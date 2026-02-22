from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Artist


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'nationality', 'birth_year', 'death_year', 'biography', 'profile_image_url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'nationality': forms.Select(attrs={'class': 'form-select'}),
            'birth_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1853',
            }),
            'death_year': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'biography': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a brief biography of the artist...',
            }),
            'profile_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/photo.jpg',
            }),
        }
        labels = {
            'name': 'Artist Name',
            'birth_year': 'Year of Birth',
            'death_year': 'Year of Death',
            'profile_image_url': 'Profile Image URL',
        }
        help_texts = {
            'death_year': 'Leave blank if the artist is still living.',
            'profile_image_url': 'Optional — link to a publicly accessible image.',
        }
        error_messages = {
            'name': {
                'required': 'Please provide the artist\'s full name.',
                'max_length': 'Name cannot exceed 200 characters.',
            },
            'birth_year': {
                'required': 'Birth year is required.',
                'invalid': 'Please enter a valid four-digit year.',
            },
            'biography': {
                'required': 'A biography is required.',
            },
        }

    def clean_birth_year(self):
        birth_year = self.cleaned_data.get('birth_year')
        current_year = timezone.now().year
        if birth_year and birth_year > current_year:
            raise ValidationError(f'Birth year cannot be in the future (max {current_year}).')
        return birth_year

    def clean(self):
        cleaned_data = super().clean()
        birth_year = cleaned_data.get('birth_year')
        death_year = cleaned_data.get('death_year')
        if birth_year and death_year:
            if death_year < birth_year:
                self.add_error('death_year', 'Death year cannot be earlier than birth year.')
        return cleaned_data


class ArtistReadOnlyForm(ArtistForm):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['created_at'] = forms.CharField(
            required=False,
            disabled=True,
            label='Added On',
            widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
        if self.instance and self.instance.pk:
            self.fields['created_at'].initial = self.instance.created_at.strftime('%d %B %Y')
