from django.db import models

from profiles.models import Profile
from animals.models import Animal


STATUS = (
    (0, "Pending"),
    (1, "Approved"),
    (2, "Rejected"),
)


class Adoption(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    message = models.TextField(
        help_text="Please include some information about yourself and why you would like to adopt this animal."
    )

    def __str__(self):
        return f"{self.user} - {self.animal}"
