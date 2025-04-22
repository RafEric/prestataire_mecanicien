

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User
@login_required
def conversation_list(request):
    # Récupérer les conversations de l'utilisateur
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

    return render(request, 'conversation_list.html', {
        'conversation_participants': conversation_participants,
    })


@login_required
def conversation_detail(request, conversation_id):
    """Affiche les détails d'une conversation (messages)"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user not in conversation.participants.all():
        return JsonResponse({'error': 'Access denied'}, status=403)

    messages = conversation.messages.order_by('timestamp')
    return render(request, 'conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })

@login_required
def start_conversation(request, user_id):
    """Crée ou récupère une conversation avec un utilisateur spécifique"""
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return JsonResponse({'error': 'Vous ne pouvez pas démarrer une conversation avec vous-même.'}, status=400)

    conversation, created = Conversation.objects.get_or_create()
    conversation.participants.add(request.user, other_user)

    return redirect('chat:conversation_detail', conversation_id=conversation.id)

@login_required
def send_message(request):
    """Envoie un message dans une conversation existante"""
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        content = request.POST.get('content')
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in conversation.participants.all():
            return JsonResponse({'error': 'Access denied'}, status=403)

        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return JsonResponse({
            'message': 'Message envoyé',
            'content': message.content,
            'sender': message.sender.username,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
