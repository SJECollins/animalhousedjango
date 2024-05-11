from django.db import models
from django.core.validators import MinValueValidator

from profiles.models import Profile


# Create your models here.
class Donation(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    amount = models.DecimalField(
        max_digits=7, decimal_places=2, validators=[MinValueValidator(0.50)]
    )
    message = models.TextField(
        blank=True, help_text="Optionally, add a message to display on the website."
    )
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city_or_town = models.CharField(max_length=100)
    county = models.CharField(max_length=100, null=True, blank=True)
    eircode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - €{self.amount:.2f}"
