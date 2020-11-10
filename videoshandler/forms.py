from django import forms
from .models import Videos

# Create your tests here.
class VideosForm(forms.ModelForm):
    class Meta:
        model=Videos
        fields=['title','youtube','url']
class SearchForm(forms.Form):
    search=forms.CharField(max_length=255)