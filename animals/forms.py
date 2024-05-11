from django import forms

from .models import Animal


class AnimalForm(forms.ModelForm):
    """A form to create or update an animal."""

    class Meta:
        model = Animal
        fields = "__all__"
