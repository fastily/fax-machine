from django.shortcuts import render

from django.middleware.csrf import get_token

from django.http import JsonResponse

# Create your views here.

def csrf_token(request):
    """Return a CSRF token for this session"""
    return JsonResponse({'token': get_token(request)})