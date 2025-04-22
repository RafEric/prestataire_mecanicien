from django.apps import AppConfig


class AuthentificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentification'
def ready(self):
        # Importez les signaux pour vous assurer qu'ils sont enregistrés
    import authentification.signals