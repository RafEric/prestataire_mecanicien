# signals.py dans une application partagée ou authentification
from django.contrib.auth.models import User
from client.models import ClientProfile  # Importez le modèle client
from prestataire.models import MecanicienProfile  # Importez le modèle mécanicien

def get_profile(self):
    if hasattr(self, 'clientprofile'):
        return self.clientprofile
    elif hasattr(self, 'mecanicienprofile'):
        return self.mecanicienprofile
    return None

User.add_to_class('profile', property(get_profile))
