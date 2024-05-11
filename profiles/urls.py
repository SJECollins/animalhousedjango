from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/", views.ProfileDetail.as_view(), name="profile_detail"),
    path("profile/update/", views.ProfileUpdate.as_view(), name="profile_update"),
]
