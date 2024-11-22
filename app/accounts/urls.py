from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import login_user,logout_user,signup  # Importez vos propres vues si nécessaire

urlpatterns = [
   # Page de connexion
    path('login/',login_user, name='login'),

    # Page de déconnexion
    path('logout/', logout_user, name='logout'),

    # Page d'inscription
    path('signup/', signup, name='signup'),

]
