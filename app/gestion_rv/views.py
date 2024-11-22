from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required 
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.models import User
from django.contrib import messages  
from twilio.rest import Client
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from gestion_rv.utils import send_email_to_user
from datetime import datetime






@login_required
def index(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request,'gestion_rv/index.html',  {'appointments': appointments})
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'gestion_rv/appointment_list.html', {'appointments': appointments})

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'gestion_rv/appointment_detail.html', {'appointment': appointment})
def create_appointment(request):
    if request.method == "POST":
        # Récupérer l'utilisateur connecté
        user = request.user

        # Récupérer la date et l'heure depuis le formulaire
        date_str = request.POST.get('date')  # Assurez-vous que la date est au bon format
        time_str = request.POST.get('time')  # Pareil pour l'heure
        description = request.POST.get('description')

        # Convertir les chaînes en objets date et time
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, "Le format de la date ou de l'heure est invalide.")
            return redirect('create_appointment')

        # Vérifier si la date et l'heure sont dans le passé
        current_datetime = datetime.now()
        appointment_datetime = datetime.combine(date, time)
        if appointment_datetime < current_datetime:
            messages.error(request, "Vous ne pouvez pas créer un rendez-vous dans le passé.")
            return redirect('create_appointment')

        # Vérifier si un rendez-vous existe déjà pour cette date et heure
        if Appointment.objects.filter(date=date, time=time).exists():
            messages.error(request, "Il y a déjà un rendez-vous à cette date et heure.")
            return redirect('create_appointment')

        try:
            # Créer un nouvel objet Appointment
            appointment = Appointment.objects.create(
                user=user,  # Associer l'utilisateur connecté
                date=date,
                time=time,
                description=description
            )
            appointment.save()

            messages.success(request, "Rendez-vous créé avec succès.")
            return redirect('success_page')  # Rediriger vers une page de succès

        except IntegrityError:
            messages.error(request, "Erreur d'intégrité. Impossible de créer ce rendez-vous.")
            return redirect('create_appointment')

    return render(request, 'gestion_rv/create_appointment.html')

def success_page(request):
    return render(request, 'gestion_rv/success_page.html')
def success_page(request):
    return render(request, 'gestion_rv/success_page.html')

def modify_appointment(request, appointment_id):
    # Récupérer le rendez-vous existant
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if request.method == 'POST':
        # Pré-remplir le formulaire avec les données existantes et les nouvelles données POST
        form = AppointmentForm(request.POST, instance=appointment)
        
        if form.is_valid():
            # Récupérer la date et l'heure mises à jour depuis le formulaire
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            
            # Vérifier si la date et l'heure sont dans le passé
            current_datetime = datetime.now()
            appointment_datetime = datetime.combine(date, time)
            if appointment_datetime < current_datetime:
                messages.error(request, "Vous ne pouvez pas modifier un rendez-vous pour une date passée.")
                return redirect('modify_appointment', appointment_id=appointment.id)

            # Vérifier si un autre rendez-vous existe déjà pour cette date et heure
            if Appointment.objects.filter(date=date, time=time).exclude(id=appointment.id).exists():
                messages.error(request, "Il y a déjà un rendez-vous à cette date et heure.")
                return redirect('modify_appointment', appointment_id=appointment.id)

            # Sauvegarder les modifications
            form.save()
            messages.success(request, "Le rendez-vous a été modifié avec succès.")
            return redirect('appointment_list')  # Rediriger vers la page des rendez-vous

    else:
        # Afficher un formulaire pré-rempli avec les données actuelles du rendez-vous
        form = AppointmentForm(instance=appointment)

    return render(request, 'gestion_rv/modify_appointment.html', {'form': form, 'appointment': appointment})
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if request.method == "POST":  # Si l'utilisateur confirme via POST
        appointment.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
        
        return redirect('index')  # Redirige vers la page d'index ou une autre page
    
    # Si GET, afficher la page de confirmation
    return render(request, 'gestion_rv/cancel_appointment.html', {'appointment': appointment})

@receiver(post_save, sender=Appointment)
def handle_rendezvous_save(sender, instance, created, **kwargs):
    if created:
        # Utilisez `instance` pour accéder à l'objet Appointment
        subject = "Confirmation de votre rendez-vous"
        message = f"Bonjour, votre rendez-vous est confirmé pour le {instance.date}."
        recipient_list = [instance.user_email]  # Assurez-vous que ce champ existe dans le modèle

        # Envoyer l'e-mail
        send_email_to_user(subject, message, recipient_list)

def handle_rendezvous_delete(sender, instance, **kwargs):
    # Envoi d'email pour une suppression
    subject = "Rendez-vous annulé"
    message = f"Votre rendez-vous du {instance.date} a été annulé."
    send_email_to_user(subject, message, [instance.user_email])  # Utilisez `instance` ici
