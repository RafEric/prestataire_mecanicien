from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MecanicienProfile
from django.core.exceptions import ObjectDoesNotExist

@login_required
def complete_profile(request):
    user = request.user
    
    try:
        mecanicien_profile = MecanicienProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        messages.error(request, "Aucun profil trouvé pour cet utilisateur.")
        return redirect('authentification:signin')

    if request.method == "POST":
        sexe = request.POST.get('sexe')
        telephone = request.POST.get('telephone')
        service = request.POST.get('service')
        speciality = request.POST.get('speciality')
        photo_profil = request.FILES.get('photo_profil')

        # Validation des champs
        if not telephone:
            messages.error(request, "Le numéro de téléphone est obligatoire.")
            return render(request, 'prestataire/complete_profile.html', {'profile': mecanicien_profile})

        if not service:
            messages.error(request, "Le service est obligatoire.")
            return render(request, 'prestataire/complete_profile.html', {'profile': mecanicien_profile})

        if not speciality:
            messages.error(request, "La spécialité est obligatoire.")
            return render(request, 'prestataire/complete_profile.html', {'profile': mecanicien_profile})

        # Mise à jour du profil
        mecanicien_profile.sexe = sexe
        mecanicien_profile.telephone = telephone
        mecanicien_profile.service = service
        mecanicien_profile.speciality = speciality

        if photo_profil:
            mecanicien_profile.photo_profil = photo_profil

        mecanicien_profile.save()

        messages.success(request, "Votre profil a été complété avec succès.")
        return redirect('authentification:signin')  # Redirige vers le tableau de bord prestataire

    return render(request, 'complete_profile.html', {'profile': mecanicien_profile})

@login_required
def dashboard(request):
    profile = request.user.mecanicienprofile

    if profile.user_type == 'prestataire' and not profile.is_approved:
        return render(request, 'waiting_approval.html')

    return render(request, 'dashboard.html')
    
