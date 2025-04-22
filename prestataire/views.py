from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MecanicienProfile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from message.models import Conversation, Message


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
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

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

        if latitude and longitude:  # Vérifie si les coordonnées existent
            mecanicien_profile.latitude = latitude
            mecanicien_profile.longitude = longitude

        if photo_profil:
            mecanicien_profile.photo_profil = photo_profil

        mecanicien_profile.save()

        messages.success(request, "Votre profil a été complété avec succès.")
        return redirect('authentification:signin')  # Redirige vers le tableau de bord prestataire

    return render(request, 'complete_profile.html', {'profile': mecanicien_profile})

# prestataire/views.py
@login_required
def dashboard(request):
    profile = request.user.mecanicienprofile

    if profile.user_type == 'prestataire' and not profile.is_approved:
        return render(request, 'waiting_approval.html')

    conversations = Conversation.objects.filter(participants=request.user)
    conversation_participants = []

    for conversation in conversations:
        # Exclure l'utilisateur actuel pour obtenir l'autre participant
        participant = conversation.participants.exclude(id=request.user.id).first()

        if participant:
            # Vérifier si le participant est un mécanicien
            if hasattr(participant, 'mecanicienprofile'):
                photo_url = participant.mecanicienprofile.photo_profil.url
            # Sinon, vérifier si le participant est un client
            elif hasattr(participant, 'clientprofile'):
                photo_url = participant.clientprofile.photo_profil.url
            else:
                # URL par défaut si aucun profil trouvé
                photo_url = 'static/photos_profil/default.jpg'

            # Ajouter la conversation et le participant à la liste
            conversation_participants.append({
                'conversation': conversation,
                'participant': participant,
                'photo_profil_url': photo_url,
            })

    return render(request, 'dashboard.html', {
        'profile': profile,
        'conversation_participants': conversation_participants
    })

def profil_mecanicien(request, pk):
    mecanicien = get_object_or_404(MecanicienProfile, pk=pk, user_type='prestataire')
    return render(request, 'profil_mecanicien.html', {'mecanicien': mecanicien})
