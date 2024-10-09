# messaging/urls.py
from django.urls import path
from .views import message_thread
app_name ="messaging"
urlpatterns = [
    path('messages/<str:recipient_username>/', message_thread, name='message_thread'),
]
