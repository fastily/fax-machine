import uuid

from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from twilio.rest import Client
from twilio.twiml.fax_response import FaxResponse

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

def home(request):
    """Displays the home page"""
    return render(request, "faxes/home.html", {})


def send(request):
    """Sends a fax"""
    print(request.POST.get("recipient"))
    print(request.FILES)

    firebase_admin.initialize_app(credentials.Certificate(settings.FIREBASE_KEYS), {'storageBucket': settings.FIREBASE_STORAGE_BUCKET})

    blob = storage.bucket().blob(str(uuid.uuid4()) + ".pdf")
    blob.upload_from_file(request.FILES.get("document"))
    blob.make_public()
    print(blob.media_link)

    fax = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN).fax.faxes.create(from_=settings.MY_NUMBER, to="+1" + request.POST.get("recipient").replace("-", ""), media_url=blob.media_link)
    print(fax.sid)

    # TODO: Send success email

    return redirect("success")

def success(request):
    """shows the successful fax sent page"""
    return render(request, "faxes/success.html")


# def fax_inbound(request):
#     """Handler for when a fax is initially recieved"""
#     fr = FaxResponse()
#     fr.receive(action="/faxes/fax_recieved")
#     return HttpResponse(content=str(fr), content_type="text/xml")


# def fax_recieved(request):
#     """Handler for when fax is done being recieved"""
#     if request.method != "POST":
#         return JsonResponse({"error": "POST only"}, status=405)

#     print(request.POST.get('MediaUrl'))

#     return JsonResponse({})


# def sent_action_callback(request):
#     pass