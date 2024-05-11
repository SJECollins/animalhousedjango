from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


def send_adoption_email(adoption):
    name = adoption.user.user.profile.name
    animal = adoption.animal.name
    contact_email = settings.DEFAULT_FROM_EMAIL
    customer_email = adoption.user.user.email
    subject = render_to_string("emails/adoption_email_subject.txt")
    body = None
    if adoption.status == 0:
        body = render_to_string(
            "emails/adoption_requested_email_body.txt",
            {"name": name, "animal": animal, "contact_email": contact_email},
        )
    elif adoption.status == 1:
        body = render_to_string(
            "emails/adoption_approved_email_body.txt",
            {"name": name, "animal": animal, "contact_email": contact_email},
        )
    else:
        body = render_to_string(
            "emails/adoption_rejected_email_body.txt",
            {"name": name, "animal": animal, "contact_email": contact_email},
        )
    send_mail(
        subject,
        body,
        contact_email,
        [customer_email],
    )
