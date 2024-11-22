from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login ,logout
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.db import IntegrityError


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': 'Ce nom d’utilisateur existe déjà.'})
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
        except IntegrityError:
            return render(request, 'accounts/signup.html', {'error': 'Erreur lors de la création du compte.'})
    return render(request, 'accounts/signup.html')

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Appelle login avec un utilisateur valide
            return redirect('index')  # Redirection après connexion réussie
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'accounts/login.html')
def logout_user(request):
        logout(request)
        return redirect('login')