from django import forms

from .models import Rating, Resource


class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "subject", "file", "type"]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
