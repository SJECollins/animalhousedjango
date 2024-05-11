from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic

from animalhouse.mixins import StaffRequiredMixin

from .models import Animal
from .forms import AnimalForm


# Create your views here.
class AnimalList(generic.ListView):
    """A view to list all animals."""

    model = Animal
    template_name = "animals/animal_list.html"


class AnimalDetail(generic.DetailView):
    """A view to show animal details."""

    model = Animal
    template_name = "animals/animal_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        available = True
        if animal.status == 1 or animal.status == 3:
            available = False
        context["available"] = available
        return context


class AnimalCreate(StaffRequiredMixin, generic.CreateView, SuccessMessageMixin):
    """A view to create a new animal."""

    model = Animal
    template_name = "generic_form.html"
    form_class = AnimalForm
    success_message = "Animal was created successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Animal"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class AnimalUpdate(StaffRequiredMixin, generic.UpdateView, SuccessMessageMixin):
    """A view to update an existing animal."""

    model = Animal
    template_name = "generic_form.html"
    form_class = AnimalForm
    success_message = "Animal was updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context["title"] = f"Update {animal.name}"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context


class AnimalDelete(StaffRequiredMixin, generic.DeleteView, SuccessMessageMixin):
    """A view to delete an animal."""

    model = Animal
    template_name = "generic_form.html"
    success_url = "/animals/"
    success_message = "Animal was deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context["title"] = f"Delete {animal.name}"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        context["delete"] = True
        return context
