from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email

class NoNewUsersAccountAdapter(DefaultAccountAdapter):

        def is_open_for_signup(self, request):
                return False

        def login(self, request, user):
                super().login(request, user)

                user.emailaddress_set.update(verified=True)
