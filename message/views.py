from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def message_thread(request, recipient_username):
    recipient = User.objects.get(username=recipient_username)  # Cherche le destinataire par son nom d'utilisateur
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by('timestamp')  # Filtre les messages entre le client et le prestataire et les trie par date

    if request.method == 'POST':
        content = request.POST['content']  # Récupère le contenu du message depuis le formulaire
        Message.objects.create(sender=request.user, recipient=recipient, content=content)  # Crée un nouveau message
        return redirect('messaging:message_thread', recipient_username=recipient.username)  # Rafraîchit la page

    return render(request, 'message_thread.html', {'messages': messages, 'recipient': recipient})  # Affiche la conversation
