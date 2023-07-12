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

# settings login session cookies variables
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600

# LDAP configuration

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

INSTALLED_APPS = [
            'django_auth_ldap',
        ] + DEFAULT_APPS

# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldaps://authusm.usm.edu"
AUTH_LDAP_BIND_DN = "CN=LINUXPROXY,OU=Service Accounts,OU=Domain Administration,DC=usm,DC=golden,DC=eagles"
AUTH_LDAP_BIND_PASSWORD = "fri10&mar06?"

# Let's start with this, and we'll add the multiple search base config shown below later on.
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "OU=Domain Users,DC=usm,DC=golden,DC=eagles", ldap.SCOPE_SUBTREE, "(samAccountName=%(user)s)"
)

# Multiple Search Bases
#AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
#    "OU=Administrative Accounts,OU=Domain Administration,DC=usm,DC=golden,DC=eagles", ldap.SCOPE_SUBTREE, "(samAccountName=%(user)s)"
#    "OU=Domain Users,DC=usm,DC=golden,DC=eagles", ldap.SCOPE_SUBTREE, "(samAccountName=%(user)s)"
#)
# Or:
# AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=users,dc=example,dc=com'

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "OU=Application Groups,OU=Domain Groups,DC=usm,DC=golden,DC=eagles",
    ldap.SCOPE_SUBTREE,
    "(objectClass=group)",
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")


# We could create a mailman user group to restrict who can access it. I guess this
# is what we could use for authorization. The group will be created under
# OU=Application Groups,OU=Domain Groups,DC=usm,DC=golden,DC=eagles

# Simple group restrictions
#AUTH_LDAP_REQUIRE_GROUP = "CN=App_Mailman_Users,OU=Application Groups,OU=Domain Groups,DC=usm,DC=golden,DC=eagles"
#AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "uid" : "samAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email" : "mail",
}


# We can create Mailman Admin group and add it here

#AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "CN=App_Mailman_Users,OU=Application Groups,OU=Domain Groups,DC=usm,DC=golden,DC=eagles",
#    "is_staff": "cn=App_Mailman_Staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "CN=App_Mailman_Admins,OU=Application Groups,OU=Domain Groups,DC=usm,DC=golden,DC=eagles",
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = [
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
]
