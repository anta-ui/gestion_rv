# gestion_rv/utils.py
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)
def send_email_to_user(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            'test@5sursync.com',  # Expéditeur
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email envoyé à {recipient_list}: {subject}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")
