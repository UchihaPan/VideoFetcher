from django import forms
from .models import Videos


# Create your tests here.
class VideosForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['url']
        labels = {
            'title': 'Enter the Title of The Video',
            'youtube': 'YouTube',
            'url': 'URL'
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=255)
