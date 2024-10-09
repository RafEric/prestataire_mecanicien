from django.db import models
from django.contrib.auth.models import User

class MecanicienProfile(models.Model):
    SERVICE_CHOICES = (
        ('diagnostique', 'Diagnostique'),
        ('reparation_general', 'Réparation générale'),
        ('entretien_regulier', 'Entretien régulier'),
    )
    
    SPECIALITY_CHOICES = (
        ('diesel', 'Diesel'),
        ('essence', 'Essence'),
        ('both', 'Les deux'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, default='prestataire' )  # ou ce que vous souhaitez
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M')
    telephone = models.CharField(max_length=20, null=True, blank=True)
    photo_profil = models.ImageField(upload_to='static/photos_profil/', default='static/photos_profil/defaultProfil.jpg')
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, blank=True, null=True)
    speciality = models.CharField(max_length=50, choices=SPECIALITY_CHOICES, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    approval_message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profil mécanicien de {self.user.username}"
