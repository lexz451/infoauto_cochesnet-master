from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest
from django.template.loader import render_to_string

from infoauto.common.util_email import send_email


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def send_mail(self, template_prefix, email, context):
        subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                                   context)
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()
        template_name = '{0}_message'.format(template_prefix)
        context['context'] = context
        send_email(to_email=email, subject=subject, template=template_name,
                   from_email=from_email, context=context, smtp_config_name='default')


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

