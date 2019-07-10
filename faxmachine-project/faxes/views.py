import uuid

from django.shortcuts import render, redirect
from django.conf import settings

from twilio.rest import Client
from twilio.twiml.fax_response import FaxResponse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From

def home(request):
    """Displays the home page"""
    return render(request, "faxes/home.html", {})

def send(request):
    """Sends a fax"""
    # print(request.POST.get("recipient"))
    # print(request.FILES)

    recipient = request.POST.get("recipient")

    firebase_admin.initialize_app(credentials.Certificate(settings.FIREBASE_KEYS), {'storageBucket': settings.FIREBASE_STORAGE_BUCKET})

    blob = storage.bucket().blob(str(uuid.uuid4()) + ".pdf")
    blob.upload_from_file(request.FILES.get("document"))
    blob.make_public()
    # print(blob.media_link)

    # fax = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN).fax.faxes.create(from_=settings.MY_NUMBER, to="+1" + recipient.replace("-", ""), media_url=blob.media_link)
    # print(fax.sid)

    message = Mail(
        from_email=From(settings.FROM_EMAIL_ADDRESS, settings.SENDER_NAME),
        to_emails=settings.TO_EMAIL_ADDRESS,
        subject='Confirming fax to {} was sent'.format(recipient),
        html_content='Confirming fax to {} was sent.\n\nA copy of the sent file is available <a href="{}">here</a>.'.format(recipient, blob.media_link))

    response = SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return redirect("success")

def success(request):
    """shows the successful fax sent page"""
    return render(request, "faxes/success.html")
