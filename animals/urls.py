from django.urls import path
from . import views

app_name = "animals"

urlpatterns = [
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>/", views.AnimalDetail.as_view(), name="animal_detail"),
    path("create/", views.AnimalCreate.as_view(), name="animal_create"),
    path("<int:pk>/update/", views.AnimalUpdate.as_view(), name="animal_update"),
    path("<int:pk>/delete/", views.AnimalDelete.as_view(), name="animal_delete"),
]
