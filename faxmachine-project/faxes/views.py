from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from twilio.rest import Client

from . models import SentFax, RecievedFax

def home(request):
    for fax in Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN).fax.faxes.list(limit=20):
        if fax.direction != 'inbound' or fax.status != 'received' or RecievedFax.objects.filter(sid=fax.sid).exists():
            continue

        RecievedFax(sid=fax.sid, date=fax.date_created, sender=fax.from_, document=fax.media_url).save()

    return render(request, "faxes/home.html", {"sent_faxes": SentFax.objects, "recieved_faxes": RecievedFax.objects})


def send(request):
    print(request.POST.get("recipient"))
    print(request.FILES.get("document"))

    recipient = request.POST.get("recipient")
    SentFax(recipient=recipient, document=request.FILES.get("document"), date=timezone.now()).save()

    # TODO: upload pdf here
    fax = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN).fax.faxes.create(from_=settings.MY_NUMBER, to="+1" + recipient.replace("-", ""), media_url="https://upload.wikimedia.org/wikipedia/test/4/42/JustATestPDF.pdf")

    print(fax.sid)
    return render(request, "faxes/success.html", {})

