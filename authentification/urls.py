from django.urls import path
from authentification import views
app_name = 'authentification'
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signout', views.signout, name='signout'),
    ]
