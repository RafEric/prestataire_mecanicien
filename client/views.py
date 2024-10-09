from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ClientProfile
from django.core.exceptions import ObjectDoesNotExist

@login_required
def complete_profile(request):
    user = request.user
    
    try:
        client_profile = ClientProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        messages.error(request, "Aucun profil trouvé pour cet utilisateur.")
        return redirect('authentification:signin')

    if request.method == "POST":
        sexe = request.POST.get('sexe')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        
        photo_profil = request.FILES.get('photo_profil')

        # Validation des champs
        if not telephone:
            messages.error(request, "Le numéro de téléphone est obligatoire.")
            return render(request, 'complete_profile.html', {'profile': client_profile})

        if not adresse:
            messages.error(request, "l'adresse est obligatoire.")
            return render(request, 'complete_profile.html', {'profile': client_profile})

        

        # Mise à jour du profil
        client_profile.sexe = sexe
        client_profile.telephone = telephone
       

        if photo_profil:
            client_profile.photo_profil = photo_profil

        client_profile.save()

        messages.success(request, "Votre profil a été complété avec succès.")
        return redirect('authentification:signin')  # Redirige vers le tableau de bord prestataire

    return render(request, 'complete_profile_client.html', {'profile': client_profile})

@login_required
def dashboard(request):
    

   

    return render(request, 'dashboard.html')
    
