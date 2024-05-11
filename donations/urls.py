from django.urls import path

from . import views
from .webhooks import webhook

app_name = "donations"

urlpatterns = [
    path("", views.DonationList.as_view(), name="donation_list"),
    path("new/", views.Donate.as_view(), name="donate"),
    path(
        "create_payment_intent/",
        views.create_payment_intent,
        name="create_payment_intent",
    ),
    path("cache_donation_data/", views.cache_donation_data, name="cache_donation_data"),
    path("wh/", webhook, name="donation_webhook"),
]
