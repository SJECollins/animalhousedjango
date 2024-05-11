from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Profile


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    """A view to show profile details."""

    model = Profile
    template_name = "profiles/profile_detail.html"

    def get_object(self):
        return self.request.user.profile


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    """A view to update an existing profile."""

    model = Profile
    template_name = "generic_form.html"
    fields = "__all__"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Profile"
        context["back_url"] = self.request.META.get("HTTP_REFERER", "/")
        return context
