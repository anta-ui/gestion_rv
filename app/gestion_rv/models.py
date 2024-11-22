from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField(default="00:00")  # Champ pour l'heure du rendez-vous
    user_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ['date', 'time']  # Assurez-vous de l'unicité de la combinaison date + time

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.status})"

