from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for staff
    Using LoginRequiredMixin to redirect to login if user not authenticated
    Tests if authenticated user is staff
    """

    def test_func(self):
        return self.request.user.is_staff
