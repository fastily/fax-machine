"""Handles views for the faxmachine"""

import uuid

from django.shortcuts import render, redirect
from django.conf import settings

from twilio.rest import Client

from firebase_admin import storage

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From

def home(request):
    """Displays the home page"""
    return render(request, "faxes/home.html", {"my_num": f"{settings.MY_NUMBER[2:5]}-{settings.MY_NUMBER[5:8]}-{settings.MY_NUMBER[8:]}"})

def send(request):
    """Sends a fax"""
    recipient = request.POST.get("recipient")

    blob = storage.bucket().blob(str(uuid.uuid4()) + ".pdf")
    blob.upload_from_file(request.FILES.get("document"))
    blob.make_public()

    fax = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN).fax.faxes.create(from_=settings.MY_NUMBER, to="+1" + recipient.replace("-", ""), media_url=blob.media_link)
    # print(fax.sid)

    response = SendGridAPIClient(settings.SENDGRID_API_KEY).send(Mail(
        from_email=From(settings.FROM_EMAIL_ADDRESS, settings.SENDER_NAME),
        to_emails=settings.TO_EMAIL_ADDRESS,
        subject=f'Confirming fax to {recipient} was sent',
        html_content=f'Confirming fax to {recipient} was sent.\n\nA copy of the sent file is available <a href="{blob.media_link}">here</a>.'))
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)

    return redirect("success")

def success(request):
    """shows the successful fax sent page"""
    return render(request, "faxes/success.html")
