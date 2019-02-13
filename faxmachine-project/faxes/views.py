from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "faxes/home.html", {})

def send(request):
    return render(request, "faxes/send.html", {})

def recieved(request):
    return render(request, "faxes/recieved.html", {})
