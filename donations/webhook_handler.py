from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import time

from .models import Donation
from profiles.models import Profile


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, event):
        self.self = self
        self.event = event

    def _send_confirmation_email(self, donation):
        """Send the user a confirmation email"""
        subject = render_to_string("emails/email_subject.txt")
        body = render_to_string(
            "emails/confirmation_email_body.txt",
            {"donation": donation, "contact_email": settings.DEFAULT_FROM_EMAIL},
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [donation.email],
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        save_info = False
        intent = event.data.object
        pid = intent.id
        donation_amount = intent.metadata.donation_amount
        donation_amount = float(donation_amount)
        if "save_info" in intent.metadata:
            save_info = True
        billing_details = intent.charges.data[0].billing_details

        for field, value in billing_details.address.items():
            if value == "":
                billing_details.address[field] = None

        # update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != "AnonymousUser":
            profile = Profile.objects.get(user__username=username)
            if save_info:
                profile.address1 = billing_details.address.line1
                profile.address2 = billing_details.address.line2
                profile.city_or_town = billing_details.address.city
                profile.county = billing_details.address.state
                profile.eircode = billing_details.address.postal_code
                profile.country = billing_details.address.country
                profile.phone_number = billing_details.phone
                profile.save()

        # send confirmation email
        donation_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                donation = Donation.objects.get(
                    name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    address1__iexact=billing_details.address.line1,
                    address2__iexact=billing_details.address.line2,
                    city_or_town__iexact=billing_details.address.city,
                    county__iexact=billing_details.address.state,
                    eircode__iexact=billing_details.address.postal_code,
                    country__iexact=billing_details.address.country,
                    amount=donation_amount,
                    stripe_pid__iexact=pid,
                )
                donation_exists = True
                break
            except Donation.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if donation_exists:
            print("Donation already exists in database, send email")
            self._send_confirmation_email(donation)
            return HttpResponse(
                content=f"Webhook received: {event['type']} | SUCCESS: Verified donation already in database",
                status=200,
            )

        else:
            print("Donation does not exist in database, create donation")
            donation = None
            try:
                donation = Donation.objects.create(
                    name=billing_details.name,
                    email=billing_details.email,
                    address1=billing_details.address.line1,
                    address2=billing_details.address.line2,
                    city_or_town=billing_details.address.city,
                    county=billing_details.address.state,
                    eircode=billing_details.address.postal_code,
                    country=billing_details.address.country,
                    amount=donation_amount,
                    stripe_pid=pid,
                )
                donation.message = (
                    "Donation created from webhook payment_intent.succeeded event."
                )
                donation.save()
                print("Donation created in database, send email")
                self._send_confirmation_email(donation)
                return HttpResponse(
                    content=f"Webhook received: {event['type']} | SUCCESS: Created donation in webhook",
                    status=200,
                )
            except Exception as e:
                print(f"Error creating donation: {e}")
                if donation:
                    donation.delete()
                return HttpResponse(
                    content=f"Webhook received: {event['type']} | ERROR: {e}",
                    status=500,
                )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(content=f"Webhook received: {event['type']}", status=200)
