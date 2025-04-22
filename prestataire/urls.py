from django.urls import path
from . import views
app_name= 'prestataire'
urlpatterns = [
   # path('complete-profile/<int:user_id>/', views.complete_profile_client, name='complete_profile_client'),
    # Ajoutez d'autres URLs spécifiques aux clients ici
    path('dashboard',views.dashboard, name= 'dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('mecanicien/<int:pk>/', views.profil_mecanicien, name='profil_mecanicien'),
]
