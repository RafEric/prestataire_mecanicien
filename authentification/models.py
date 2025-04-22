# Dans authentification/models.py

from django.contrib.auth.models import User

def get_profile(self):
    # Vérifie quel profil existe pour cet utilisateur
    if hasattr(self, 'clientprofile'):
        return self.clientprofile
    elif hasattr(self, 'mecanicienprofile'):
        return self.mecanicienprofile
    return None

# Ajout de la méthode `profile` à `User` pour accéder au profil directement
User.add_to_class('profile', property(get_profile))
