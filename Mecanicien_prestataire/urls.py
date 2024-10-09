"""
URL configuration for Mecanicien_prestataire project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings
from .views import*
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', acceuil , name ="index"),
    path('service', service , name ="service"),
    path('authentification/', include('authentification.urls')),
    path('client/', include('client.urls')),  # Inclure les URLs de l'application Client
    path('prestataire/', include('prestataire.urls')),  # Inclure les URLs de l'application Prestataire
     path('api/', include('message.urls')),
    
   # path('mecaniciens_proches/', mecaniciens_proches, name='mecaniciens_proches'),
   # path('authentification/', include('authentification.urls')),
   # path('admin_app/', include('admin_app.urls')),
   # path('prestataire_app/', include('prestataire_app.urls')),
  
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
