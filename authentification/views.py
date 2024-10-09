from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from Mecanicien_prestataire import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken
from .models import*
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from prestataire.models import MecanicienProfile 
from client.models import ClientProfile # Assurez-vous d'importer correctement generateToken



from django.utils.encoding import force_str

 # Assurez-vous d'avoir ce token configuré

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')

        # Validation des données du formulaire
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d\'utilisateur est déjà pris.')
            return render(request, 'authentification/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà associé à un compte.')
            return render(request, 'authentification/signup.html')

        if password != confirm_password:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'authentification/signup.html')

        # Création de l'utilisateur
        my_user = User.objects.create_user(username=username, email=email, password=password)
        my_user.is_active = False  # L'utilisateur doit d'abord activer son compte
        my_user.save()

        if user_type == 'client':
            profile = ClientProfile.objects.create(user=my_user)
        elif user_type == 'prestataire':
            profile = MecanicienProfile.objects.create(user=my_user)
        else:
            messages.error(request, "Type d'utilisateur non reconnu.")
            return render(request, 'authentification/signup.html')
        # Envoi de l'e-mail de confirmation
        current_site = get_current_site(request)
        email_subject = "Confirmez votre email"
        message_confirm = render_to_string('authentification/emailConfimation.html', {
            'name': my_user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user),
        })

        email = EmailMessage(
            email_subject,
            message_confirm,
            settings.EMAIL_HOST_USER,
            [my_user.email],
        )
        email.fail_silently = False
        email.send()
        if user_type == 'prestataire':
            admin_email = settings.ADMIN_EMAIL
            subject = "Nouvelle inscription de prestataire en attente d'approbation"
            message = f"Un nouveau prestataire {my_user.first_name} {my_user.last_name} s'est inscrit et est en attente d'approbation."
            send_mail(subject, message, settings.EMAIL_HOST_USER, [admin_email], fail_silently=False)
        messages.success(request, "Votre compte a été créé avec succès. Veuillez vérifier votre email pour l'activer.")
        return redirect('authentification:signin')  # Redirige vers la page de connexion pour l'activation par email

    return render(request, 'authentification/signup.html')
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            my_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur correspondant n'a été trouvé.")
            return render(request, 'authentification/signin.html')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                # Récupération du profil en fonction du type d'utilisateur
                try:
                    if hasattr(user, 'mecanicienprofile'):
                        profile = user.mecanicienprofile
                    elif hasattr(user, 'clientprofile'):
                        profile = user.clientprofile
                    else:
                        messages.error(request, "Profil utilisateur non trouvé.")
                        return redirect('authentification:signin')

                    # Vérification du type d'utilisateur et redirection en fonction
                    if profile.user_type == 'client':
                        login(request, user)
                        return redirect('index')  # Redirige vers le tableau de bord du client
                    elif profile.user_type == 'prestataire':
                        if not profile.is_approved:
                            messages.error(request, "Votre compte n'a pas encore été approuvé par l'administrateur.")
                            return render(request, 'authentification/signin.html')
                        
                        login(request, user)
                        return redirect('prestataire:dashboard')  # Redirige vers le tableau de bord du prestataire
                    else:
                        messages.error(request, "Type d'utilisateur non reconnu.")
                        return redirect('authentification:signin')

                except Exception as e:
                    messages.error(request, "Erreur lors de la récupération du profil utilisateur.")
                    return redirect('authentification:signin')

            else:
                messages.error(request, "Vous n'avez pas confirmé votre email. Faites-le afin d'activer votre compte.")
                return render(request, 'authentification/signin.html')
        else:
            messages.error(request, 'Mauvaise authentification.')
            return render(request, 'authentification/signin.html')

    return render(request, 'authentification/signin.html')



# Assurez-vous d'importer votre générateur de jetons



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        if not my_user.is_active:
            my_user.is_active = True        
            my_user.save()
            login(request, my_user)

            # Afficher un message de succès et rediriger selon le type d'utilisateur
            messages.success(request, "Votre compte est activé. Veuillez compléter votre profil.")
            
            # Vérifier si l'utilisateur est un client ou un prestataire
            try:
                if hasattr(my_user, 'mecanicienprofile'):
                    return redirect('prestataire:complete_profile')  # Redirige vers la vue prestataire
                elif hasattr(my_user, 'clientprofile'):
                    return redirect('client:complete_profile')  # Redirige vers la vue client
            except Exception as e:
                messages.error(request, f"Erreur lors de la redirection : {str(e)}")
                return redirect('authentification:signin')
        else:
            messages.info(request, "Votre compte est déjà activé.")
            return redirect('authentification:signin')
    else:
        messages.error(request, "Échec de l'activation ou le jeton est invalide.")
        return redirect('authentification:signup')

def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('index')