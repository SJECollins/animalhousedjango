from django.urls import path

from . import views

app_name = "adoptions"

urlpatterns = [
    path("", views.AdoptionList.as_view(), name="list"),
    path("<int:pk>/", views.AdoptionDetail.as_view(), name="detail"),
    path("create/<int:pk>/", views.AdoptionCreate.as_view(), name="create"),
    path("update/<int:pk>/", views.AdoptionUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", views.AdoptionDelete.as_view(), name="delete"),
]
