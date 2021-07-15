from django import forms

from core.music.models import Song

class AddSongForm(forms.ModelForm):
    artists = forms.CharField(
        max_length=140, 
        label='Artists', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Artists',
                'autocomplete': 'off',
                'autofocus': 'true',
                'autocapitalize': 'off'
            }
        )
    ) 
    title = forms.CharField(
        required=True,
        max_length=140, 
        label='Song title', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Song title',
                'autocomplete': 'off',
                'autocapitalize': 'off'
            }
        )
    ) 
    spotify = forms.URLField(
        required=False,
        max_length=180, 
        label='Spotify url', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Spotify url',
                'autocomplete': 'off',
                'autocapitalize': 'off'
            }
        )
    ) 
    soundcloud = forms.URLField(
        required=False,
        max_length=180, 
        label='Soundclound url', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Soundclound url',
                'autocomplete': 'off',
                'autocapitalize': 'off'
            }
        )
    ) 
    youtube = forms.URLField(
        required=False,
        max_length=180, 
        label='YouTube url', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'YouTube url',
                'autocomplete': 'off',
                'autocapitalize': 'off'
            }
        )
    ) 
    cover_art = forms.ImageField(
        required=False, 
        widget=forms.FileInput(
            attrs={
                'required': 'false',
                'onchange': 'processImage()',
                'id': 'selected-image',
                'required': 'false'
            }
        )
    )
    class Meta:
        model = Song
        fields = (
            'artists',
            'title',
            'genre',
            'spotify',
            'soundcloud',
            'youtube',
            'cover_art',
        )