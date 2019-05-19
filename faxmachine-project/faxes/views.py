from django.shortcuts import render
from django.utils import timezone

from . models import SentFax, RecievedFax

def home(request):
    return render(request, "faxes/home.html", {"sent_faxes": SentFax.objects, "recieved_faxes": RecievedFax.objects})

def send(request):
    print(request.POST.get("recipient"))
    print(request.FILES.get("document"))

    SentFax(recipient=request.POST.get("recipient"), document=request.FILES.get("document"), date=timezone.now()).save()

    return render(request, "faxes/success.html", {})