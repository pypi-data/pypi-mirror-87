from typing import Optional

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

from NEMO.models import User


class NEMOAccountAdapter(DefaultAccountAdapter):

	def is_open_for_signup(self, request):
		"""
		Checks whether or not the site is open for signups.

		Next to simply returning True/False you can also intervene the
		regular flow by raising an ImmediateHttpResponse
		"""
		return False

	def get_from_email(self):
		return settings.SERVER_EMAIL if settings.SERVER_EMAIL else settings.DEFAULT_FROM_EMAIL

	def add_message(self, request, level, message_template, message_context=None, extra_tags=""):
		# Override this method to make it safe in case no request is passed
		if request:
			super().add_message(request, level, message_template, message_context, extra_tags)


class NEMOSocialAccountAdapter(DefaultSocialAccountAdapter):

	def is_auto_signup_allowed(self, request, sociallogin):
		return False

	def pre_social_login(self, request, sociallogin):
		if settings.AUTO_CONNECT_VERIFIED_EMAIL:
			# social account already exists, so this is just a login
			if sociallogin.is_existing:
				return

			# some social logins don't have an email address
			if not sociallogin.email_addresses:
				return

			# find the first verified email that we get from this sociallogin
			verified_email: Optional[str] = None
			for email in sociallogin.email_addresses:
				if email.verified:
					verified_email = email.email
					break

			# if not found, take a look in extra data
			if not verified_email and sociallogin.account and sociallogin.account.extra_data:
				extra_data = sociallogin.account.extra_data
				if 'email_verified' in extra_data and 'email' in extra_data and bool(extra_data['email_verified']):
					verified_email = extra_data['email']

			# no verified emails found, nothing more to do
			if not verified_email:
				return

			# check first if given email address already exists as a verified email on an existing user's account
			verified_user: Optional[User] = None
			try:
				existing_email = EmailAddress.objects.get(email__iexact=verified_email, verified=True)
				verified_user = existing_email.user
			except EmailAddress.DoesNotExist:
			# next check if there is a superuser with that email, if the setting is enabled
				if settings.TRUST_SUPERUSERS_EMAIL:
					try:
						superuser = User.objects.get(is_active=True, is_superuser=True, email=verified_email)
						EmailAddress.objects.create(user=superuser, email=verified_email, verified=True, primary=True)
						verified_user = superuser
					except User.DoesNotExist:
						pass

			# no user found with a verified email, nothing more to do
			if not verified_user:
				return

			# we found a user, connect this new social login
			sociallogin.connect(request, verified_user)