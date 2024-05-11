import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_POST
import stripe

from .models import Donation
from .forms import DonationForm
from profiles.models import Profile


class DonationList(generic.ListView):
    model = Donation
    template_name = "donations/donation_list.html"


class Donate(generic.View):

    def get(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        form = None
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                form = DonationForm(
                    initial={
                        "name": profile.full_name,
                        "email": profile.user.email,
                        "phone": profile.phone_number,
                        "address1": profile.address1,
                        "address2": profile.address2,
                        "city_or_town": profile.city_or_town,
                        "county": profile.county,
                        "eircode": profile.eircode,
                        "country": profile.country,
                    }
                )
            except Profile.DoesNotExist:
                form = DonationForm()
        else:
            form = DonationForm()

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing. Did you forget to set it in your environment?",
            )
        context = {
            "form": form,
            "stripe_public_key": stripe_public_key,
        }
        return render(request, "donations/donation_form.html", context)

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            pid = request.POST.get("client_secret").split("_secret")[0]
            donation.stripe_pid = pid
            donation.save()

            if "save_info" in request.POST:
                profile = Profile.objects.get(user=request.user)
                profile.phone_number = donation.phone
                profile.address1 = donation.address1
                profile.address2 = donation.address2
                profile.city_or_town = donation.city_or_town
                profile.county = donation.county
                profile.eircode = donation.eircode
                profile.country = donation.country
                profile.save()
            messages.success(
                request, f"Your donation of €{donation.amount:.2f} was successful!"
            )
            return redirect(reverse("donations:donation_list"))
        else:
            context = {
                "form": form,
                "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
                "client_secret": "test",
            }
            messages.error(
                request,
                "There was an error with your form. Please double check your information.",
            )
            return render(request, "donations/donation_form.html", context)


def create_payment_intent(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    donation_amount = json.loads(request.body)["donation_amount"]

    intent = stripe.PaymentIntent.create(
        amount=round(float(donation_amount) * 100),
        currency="eur",
    )
    return JsonResponse({"client_secret": intent.client_secret})


@require_POST
def cache_donation_data(request):
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        save_info = None
        data = json.loads(request.body)
        pid = data["client_secret"].split("_secret")[0]
        donation_amount = data["donation_amount"]
        if "save_info" in data:
            save_info = data["save_info"]

        metadata = {
            "donation_amount": donation_amount,
        }
        if "save_info" in request.POST:
            metadata["save_info"] = save_info
        if request.user.is_authenticated:
            metadata["username"] = request.user
        else:
            metadata["username"] = "AnonymousUser"

        stripe.PaymentIntent.modify(
            pid,
            metadata=metadata,
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. Please try again later.",
        )
        return HttpResponse(content=e, status=400)
