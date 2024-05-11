from typing import Any
from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):
    save_info = forms.BooleanField(label="Save my information", required=False)

    class Meta:
        model = Donation
        fields = (
            "name",
            "email",
            "phone",
            "amount",
            "message",
            "address1",
            "address2",
            "city_or_town",
            "county",
            "eircode",
            "country",
        )
