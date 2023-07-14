from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

'''
This script will trigger when a ldap user logs in for the first time
and make an API call to verify the user's email address
'''



@receiver(user_logged_in)
def email_verify(sender, request, user, **kwargs):
    if user.last_login is None:
        # code to verify email
        email = user.email
        
