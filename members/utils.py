import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return ''.join([str(random.randint(0,9)) for _ in range(6)])



def send_otp_email(email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER  
    recipient_list = [email] 
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)