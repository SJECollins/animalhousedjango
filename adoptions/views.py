from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from animalhouse.mixins import StaffRequiredMixin

from .emails import send_adoption_email

from .models import Adoption
from .forms import AdoptionForm

from animals.models import Animal
from profiles.models import Profile


class AdoptionList(LoginRequiredMixin, generic.ListView):
    model = Adoption
    template_name = "adoptions/adoption_list.html"

    def get_queryset(self):
        adoption_list = Adoption.objects.all()
        if self.request.user.is_staff:
            return Adoption.objects.all()
        else:
            profile = Profile.objects.get(user=self.request.user)
            adoption_list = Adoption.objects.filter(user=profile)
        return adoption_list


class AdoptionDetail(LoginRequiredMixin, generic.DetailView):
    model = Adoption
    template_name = "adoptions/adoption_detail.html"


class AdoptionCreate(LoginRequiredMixin, generic.CreateView, SuccessMessageMixin):
    model = Adoption
    template_name = "generic_form.html"
    form_class = AdoptionForm
    success_message = "Your adoption request has been sent!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = Animal.objects.get(pk=self.kwargs["pk"])
        context["animal"] = animal
        context["title"] = f"Adoption request for {animal.name}"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        animal = Animal.objects.get(pk=self.kwargs["pk"])
        form.instance.animal = animal
        form.instance.user = Profile.objects.get(user=self.request.user)
        self.object.save()
        send_adoption_email(self.object)
        return HttpResponseRedirect(self.get_success_url())


class AdoptionUpdate(StaffRequiredMixin, generic.UpdateView):
    model = Adoption
    template_name = "generic_form.html"
    fields = ["status"]
    success_message = "Adoption request was updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.object.animal
        context["title"] = f"Update adoption request for {animal.name}"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context

    def form_valid(self, form):
        initial_status = self.get_object().status
        new_status = form.cleaned_data["status"]
        if initial_status != new_status:
            send_adoption_email(self.object)
        return super().form_valid(form)


class AdoptionDelete(LoginRequiredMixin, generic.DeleteView):
    model = Adoption
    template_name = "generic_form.html"
    success_message = "Adoption request was deleted successfully!"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.object.animal
        context["title"] = f"Delete adoption request for {animal.name}"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        context["delete"] = True
        return context
