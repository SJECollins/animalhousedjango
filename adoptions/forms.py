from django import forms

from .models import Adoption


class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }
