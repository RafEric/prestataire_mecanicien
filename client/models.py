from django.db import models
from django.contrib.auth.models import User

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, default="client")  # ou ce que vous souhaitez
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M')
    telephone = models.CharField(max_length=20, null=False, blank=False, default="Non spécifié")  # Valeur par défaut ajoutée
    adresse = models.CharField(max_length=255, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='static/photos_clients/', default='static/photos_clients/defaultClient.jpg')

    def __str__(self):
        return f"Profil client de {self.user.username}"
