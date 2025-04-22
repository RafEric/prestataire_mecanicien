from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('send/', views.send_message, name='send_message'),
]
