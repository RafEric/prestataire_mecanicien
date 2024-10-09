from django.urls import path
from . import views
app_name= 'client'
urlpatterns = [
   # path('complete-profile/<int:user_id>/', views.complete_profile_client, name='complete_profile_client'),
    # Ajoutez d'autres URLs spécifiques aux clients ici
    path('dashboard',views.dashboard, name= 'dashboard'),
    path('completer_profil_client/', views.complete_profile, name='complete_profile'),
]
