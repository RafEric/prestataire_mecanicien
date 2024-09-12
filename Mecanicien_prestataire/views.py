from authentification.models import *
from django.shortcuts import redirect, render

def acceuil(request, *args, **kwargs):
    #mecanicien = Profile.objects.filter(user_type='prestataire', is_approved=True)[:3]
    return render(request, 'index.html' )

def service(request, *args, **kwargs):
    
    return render(request, 'service.html' )