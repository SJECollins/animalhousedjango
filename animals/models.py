from django.db import models


STATUS = (
    (0, "Available"),
    (1, "Adopted"),
    (2, "Fostered"),
    (3, "On hold"),
)


# Create your models here.
class Animal(models.Model):
    """A model to represent an animal."""

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to="animals")
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.name
