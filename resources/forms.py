from django import forms

from .models import Rating, Resource


class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "subject", "file", "type"]

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        if not uploaded.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Only PDF files are allowed.")
        return uploaded


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["value"]
