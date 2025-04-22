import random
from faker import Faker
from django.contrib.auth.models import User
from prestataire.models import MecanicienProfile

fake = Faker()

for _ in range(10):  # Générer 10 mécaniciens
    username = fake.user_name()
    email = fake.email()
    password = "password123"

    user = User.objects.create_user(username=username, email=email, password=password)

    mecanicien = MecanicienProfile.objects.create(
        user=user,
        sexe=random.choice(['M', 'F']),
        telephone=fake.phone_number(),
        service=random.choice(['diagnostique', 'reparation_general', 'entretien_regulier']),
        speciality=random.choice(['diesel', 'essence', 'both']),
        is_approved=random.choice([True, False]),
        approval_message=fake.sentence() if random.choice([True, False]) else None,
        latitude=fake.latitude(),
        longitude=fake.longitude()
    )

    print(f"Utilisateur {user.username} ajouté !")

# Vérifier le nombre total de mécaniciens après ajout
print("Nombre total de mécaniciens :", MecanicienProfile.objects.count())
