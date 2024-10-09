from django.contrib import admin

# Register your models here.
from django.urls import path, reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib.admin import ModelAdmin
from prestataire.models import MecanicienProfile
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
import logging

logger = logging.getLogger(__name__)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'is_approved', 'pending_approval', 'activate_button')
    list_filter = ('user_type', 'is_approved')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('activate/<int:profile_id>/', self.admin_site.admin_view(self.activate_prestataire), name='activate-prestataire'),
        ]
        return custom_urls + urls

    def activate_button(self, obj):
        if obj.user_type == 'prestataire' and not obj.is_approved:
            return format_html(
                '<a class="button" href="{}">Activer</a>',
                reverse('admin:activate-prestataire', args=[obj.pk]),
            )
        return 'Approuvé'
    activate_button.short_description = 'Activation'
    activate_button.allow_tags = True

    def activate_prestataire(self, request, profile_id, *args, **kwargs):
        profile = self.get_object(request, profile_id)
        if profile:
            with transaction.atomic():
                profile.is_approved = True
                profile.approval_message = "Votre compte a été approuvé. Vous pouvez maintenant vous connecter."
                profile.save()
                subject = "Votre compte a été approuvé"
                message = f"Bonjour {profile.user.first_name},\n\nVotre compte prestataire a été approuvé. Vous pouvez maintenant vous connecter et utiliser votre compte.\n\nMerci,\nL'équipe"
                from_email = settings.EMAIL_HOST_USER
                to_list = [profile.user.email]

                try:
                    send_mail(subject, message, from_email, to_list, fail_silently=False)
                    messages.success(request, f"Le compte de {profile.user.first_name} {profile.user.last_name} a été approuvé.")
                except Exception as e:
                    messages.error(request, f"Erreur lors de l'envoi de l'email à {profile.user.email}. Veuillez réessayer.")
                    logger.error(f"Erreur lors de l'envoi de l'email à {profile.user.email}: {e}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def pending_approval(self, obj):
        if obj.user_type == 'prestataire' and not obj.is_approved:
            return format_html('<span style="color: red;">En attente d\'approbation</span>')
        return 'Approuvé'
    pending_approval.short_description = 'Statut d\'approbation'

admin.site.register(MecanicienProfile, ProfileAdmin)
