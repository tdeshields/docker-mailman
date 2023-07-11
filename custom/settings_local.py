#Disabling user sign-up. Already existing users are still allowed to login.
ACCOUNT_ADAPTER = 'django_mailman3.views.user_adapter.DisableSignupAdapter'
# Enable debug if needed
# DEBUG = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ALLOWED_HOSTS = ['*']

# cross site cookies
CSRF_TRUSTED_ORIGINS = [
        "https://listdev.usm.edu",
]
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': "/opt/mailman-web-data/fulltext_index",
    },
}
#Disable social SSO login
MAILMAN_WEB_SOCIAL_AUTH = []

# disabling email verification
ACCOUNT_EMAIL_VERIFICATION = 'none'
MAILMAN_EMAIL_RESTRICTIONS = 'none'

# setting time zone globally
TIME_ZONE = 'America/Chicago'
