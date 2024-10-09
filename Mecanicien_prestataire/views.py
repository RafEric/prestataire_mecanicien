from prestataire.models import *
from django.shortcuts import redirect, render

def acceuil(request, *args, **kwargs):
    mecanicien = MecanicienProfile.objects.filter(user_type='prestataire', is_approved=True)[:5]
    return render(request, 'index.html' , {'mecanicien':mecanicien} )

def service(request, *args, **kwargs):
    
    return render(request, 'service.html' )